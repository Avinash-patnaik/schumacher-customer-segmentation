import os
import pandas as pd
import chromadb
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

class TextProcessor:
    def __init__(self, model_id="sentence-transformers/all-MiniLM-L6-v2"):
        """
        Senior Implementation: Decoupled Embedding Logic using HF Inference API.
        """
        self.token = os.getenv("HF_TOKEN")
        self.client = InferenceClient(token=self.token)
        self.model_id = model_id
        self.db_client = chromadb.PersistentClient(path=os.getenv("CHROMA_PATH"))
        self.collection = self.db_client.get_or_create_collection(name="product_taxonomy")

    def generate_embeddings(self, text: str):
        """Fetches embeddings from Hugging Face Inference API."""
        return self.client.feature_extraction(text, model=self.model_id)

    def upsert_catalog(self, df: pd.DataFrame):
        """
        Professional Batch Processing: Indexes product metadata for RAG.
        Uses columns identified in data audit: motif, scale, classification.
        """
        documents = []
        metadatas = []
        ids = []

        for _, row in df.iterrows():
            content = f"{row['category_name']} {row['motif']} motif. Scale: {row['scale']}. Color: {row['color_name']}"
            documents.append(content)
            ids.append(str(row['item_number']))
            metadatas.append({"price": row['price_usd'], "type": row['type']})

        embeddings = [self.generate_embeddings(doc) for doc in documents]
        self.collection.add(
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    def semantic_search(self, query: str, top_k=5):
        """Executes a natural language search against the Schumacher catalog."""
        query_vector = self.generate_embeddings(query)
        return self.collection.query(query_embeddings=[query_vector], n_results=top_k)