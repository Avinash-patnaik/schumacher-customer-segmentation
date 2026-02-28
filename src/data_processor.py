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
        
    def merge_data(self):
        try:
            self.df_trans['shipped_dt'] = pd.to_datetime(self.df_trans['shipped_dt'])
            self.df_trans['netrevenue'] = self.df_trans['netrevenue'].fillna(0)
            
            self.df_master = self.df_trans.merge(self.df_cust, on='customer_id', how='left')
            self.df_master = self.df_master.merge(self.df_prod, on='product_id', how='left')
            self.df_master.to_csv(os.path.join(self.processed_data, 'master.csv'), index=False)
            print("Data merged and saved successfully.")
        except Exception as e:
            print(f"Error merging data: {e}")
            raise e