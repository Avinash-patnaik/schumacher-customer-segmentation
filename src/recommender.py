import pandas as pd
import numpy as np
import os

class SchumacherRecommender:
    def __init__(self, data_path=None):
        """
        Initialize the recommender. 
        Auto-detects path to handle being called from root or notebooks.
        """
        if data_path is None:
            paths_to_check = [
                'data/processed/notebooks/final_analytics_data.parquet',
                '../data/processed/notebooks/final_analytics_data.parquet'
            ]
            for p in paths_to_check:
                if os.path.exists(p):
                    data_path = p
                    break
        
        if not data_path or not os.path.exists(data_path):
            raise FileNotFoundError("Could not find final_analytics_data.parquet. Check your paths.")

        print(f"🚀 Loading Schumacher Intelligence from {data_path}...")
        self.df = pd.read_parquet(data_path)
        self.sales_df = self.df[self.df['type'] == 'SALE']
        self.cluster_map = {
            0.0: "💎 Champions (VIPs)",
            1.0: "🌱 New Prospects",
            2.0: "⚠️ At-Risk High Value",
            3.0: "💤 Hibernating/Lost",
            4.0: "🔄 Loyal General Trade"
        }

    def get_account_summary(self, trade_account_id):
        """Returns key metrics for a specific designer to show in the app."""
        account_data = self.df[self.df['trade_account_id'] == trade_account_id]
        if account_data.empty:
            return None
        info = account_data.iloc[0]
        summary = {
            'cluster_name': self.cluster_map.get(info['Cluster'], "Unknown"),
            'total_spend': account_data['netrevenue'].sum(),
            'sample_count': int(account_data[account_data['type'] == 'SAMPLE'].shape[0]),
            'top_category': account_data['category_name'].mode()[0] if not account_data['category_name'].empty else "N/A"
        }
        return summary

    def get_cluster_top_sellers(self, cluster_id, top_n=10):
        """Finds most popular items within a designer's peer group."""
        cluster_sales = self.sales_df[self.sales_df['Cluster'] == cluster_id]
        top_items = cluster_sales.groupby(['item_number', 'category_name', 'motif']).agg({
            'quantity': 'sum',
            'trade_account_id': 'nunique'
        }).rename(columns={'trade_account_id': 'unique_buyers'})
        
        return top_items.sort_values(by='unique_buyers', ascending=False).head(top_n).reset_index()

    def recommend_for_account(self, trade_account_id, top_n=5):
        """
        Main logic: Cluster-based filtering + History exclusion.
        """
        account_info = self.df[self.df['trade_account_id'] == trade_account_id]
        if account_info.empty:
            return "Account ID not found."
        
        cluster_id = account_info['Cluster'].iloc[0]
    
        recommendations = self.get_cluster_top_sellers(cluster_id, top_n=20)

        purchased = set(account_info[account_info['type'] == 'SALE']['item_number'].unique())
        final_recs = recommendations[~recommendations['item_number'].isin(purchased)]
        
        return final_recs.head(top_n)

if __name__ == "__main__":
    try:
        rec_sys = SchumacherRecommender()
        test_id = rec_sys.df['trade_account_id'].iloc[0]
        print(f"\nAccount Summary for {test_id}:")
        print(rec_sys.get_account_summary(test_id))
        print(f"\nTop Recommendations:")
        print(rec_sys.recommend_for_account(test_id))
    except Exception as e:
        print(f"Setup Error: {e}")