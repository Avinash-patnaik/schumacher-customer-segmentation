import pandas as pd 
import os

class DataProcessor:
    def __init__(self, raw_data='data/raw', processed_data='data/processed'):
        self.raw_data = raw_data
        self.processed_data = processed_data
        self.master_df = None   
        
        os.makedirs(self.processed_data, exist_ok=True)
        
    def load_data(self):
        try:
            self.df_trans = pd.read_csv(os.path.join(self.raw_data, 'transactions.csv'))
            self.df_cust = pd.read_csv(os.path.join(self.raw_data, 'customer_master.csv'))
            self.df_prod = pd.read_csv(os.path.join(self.raw_data, 'item_master.csv'))
            print("Data loaded successfully.")
        except Exception as e:
            print(f"Error loading data: {e}")
            raise e
        
    def merge_data(self, force_refresh=False):
        """
        Module 1: Smart Merging
        Checks if the processed file exists; if not, performs the 2M row merge.
        :param force_refresh: Set to True to bypass the check and merge again.
        """
        output_file = os.path.join(self.processed_data, 'master_analytical_file.csv')

        if os.path.exists(output_file) and not force_refresh:
            print(f"📦 Processed data found at {output_file}. Loading existing file...")
            self.df_master = pd.read_csv(output_file, low_memory=False)
            # Ensure date conversion persists after loading from CSV
            self.df_master['shipped_dt'] = pd.to_datetime(self.df_master['shipped_dt'])
            print(f"✅ Loaded {len(self.df_master):,} records from disk.")
            return

        try:
            print("⚙️ Processing 2M records... This may take a moment.")
            self.df_trans['shipped_dt'] = pd.to_datetime(self.df_trans['shipped_dt'])
            self.df_trans['netrevenue'] = self.df_trans['netrevenue'].fillna(0)
            
            # Left Join Chain
            self.df_master = self.df_trans.merge(self.df_cust, on='trade_account_id', how='left')
            self.df_master = self.df_master.merge(self.df_prod, on='item_number', how='left')
            
            self.df_master['business_type'] = self.df_master['business_type'].fillna('Unknown')
            self.df_master['category_name'] = self.df_master['category_name'].fillna('Uncategorized')
            
            self.df_master.to_csv(output_file, index=False)
            print(f"💾 Merge complete. Saved new master file to {output_file}")
            
        except Exception as e:
            print(f"❌ Error during smart merge: {e}")
            raise e
        
# Main Execution (for testing)
if __name__ == "__main__":
    engine = DataProcessor()
    engine.load_data()
    engine.merge_data()