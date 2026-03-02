import os
import chromadb
from PIL import Image
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

class VisionMatcher:
    def __init__(self, model_id="openai/clip-vit-base-patch32"):
        """
        Advanced Vision Implementation: Uses CLIP for zero-shot visual similarity.
        """
        self.client = InferenceClient(token=os.getenv("HF_TOKEN"))
        self.model_id = model_id
        self.db_client = chromadb.PersistentClient(path=os.getenv("CHROMA_PATH"))
        self.collection = self.db_client.get_or_create_collection(name="product_visuals")

    def get_image_embedding(self, image_path: str):
        """Encodes an image into a vector using HF Inference."""
        with open(image_path, "rb") as f:
            image_data = f.read()
        return self.client.feature_extraction(image_data, model=self.model_id)

    def index_images(self, image_dir: str):
        """
        Indexes the visual assets stored in data/images/.
        """
        valid_extensions = ('.jpg', '.jpeg', '.png')
        for filename in os.listdir(image_dir):
            if filename.lower().endswith(valid_extensions):
                path = os.path.join(image_dir, filename)
                item_id = filename.split('.')[0] 
                
                embedding = self.get_image_embedding(path)
                self.collection.add(
                    embeddings=[embedding],
                    ids=[item_id],
                    metadatas=[{"path": path}]
                )

    def match_inspiration(self, upload_path: str, n_results=3):
        """
        The 'Designer Inspiration' tool: Matches an uploaded photo to catalog items.
        """
        query_embedding = self.get_image_embedding(upload_path)
        return self.collection.query(query_embeddings=[query_embedding], n_results=n_results)