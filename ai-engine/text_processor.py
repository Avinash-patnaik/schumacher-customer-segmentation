import pandas as pd 
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.utils import embedding_functions

class TextProcessor:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        """
        Initializes the NLP model and the Vector Database.
        """
        self.model = SentenceTransformer(model_name)
        self.client = chromadb.PersistentClient(path="../data/chromadb")
        self.collection = self.client.get_or_create_collection(name="product_descriptions")

    def prepare_metadata(self, df):
        """
        Combines product attributes into a rich text string for embedding.
        """
        df['combined_text'] = df.apply(lambda x: 
            f"{x['category_name']} in {x['color_name']} color. "
            f"Style is {x['classification']} with a {x['motif']} motif. "
            f"Scale is {x['scale']}.", axis=1)
        return df

    def build_index(self, df):
        """
        Generates embeddings and stores them in ChromaDB.
        """
        descriptions = df['combined_text'].tolist()
        ids = df['item_number'].astype(str).tolist()
        
        self.collection.add(
            documents=descriptions,
            ids=ids,
            metadatas=df[['item_number', 'price_usd', 'category_name']].to_dict('records')
        )
        print(f"Successfully indexed {len(ids)} products.")

    def search(self, query, n_results=5):
        """
        Semantically searches for products based on a natural language query.
        Example: 'Modern blue fabric with a large geometric pattern'
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results