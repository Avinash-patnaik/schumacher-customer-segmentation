import torch
from PIL import Image
import open_clip
import chromadb
import os

class VisionMatcher:
    def __init__(self, model_name='ViT-B-32', pretrained='laion2b_s34b_b79k'):
        """
        Initializes the CLIP model for visual feature extraction.
        CLIP is ideal as it understands the relationship between images and text.
        """
        self.model, _, self.preprocess = open_clip.create_model_and_transforms(
            model_name, pretrained=pretrained
        )
        self.tokenizer = open_clip.get_tokenizer(model_name)
        self.client = chromadb.PersistentClient(path="../data/chromadb")
        self.collection = self.client.get_or_create_collection(name="product_visuals")

    def encode_image(self, image_path):
        """
        Converts an image file into a normalized vector (embedding).
        """
        image = self.preprocess(Image.open(image_path)).unsqueeze(0)
        with torch.no_grad():
            image_features = self.model.encode_image(image)
            image_features /= image_features.norm(dim=-1, keepdim=True)
        return image_features.cpu().numpy().flatten().tolist()

    def index_product_images(self, image_folder="../data/images/"):
        """
        Iterates through the product images and stores their vectors in ChromaDB.
        """
        image_files = [f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.png'))]
        
        for img_file in image_files:
            img_path = os.path.join(image_folder, img_file)
            item_id = img_file.split('.')[0] 
            
            embedding = self.encode_image(img_path)
            
            self.collection.add(
                embeddings=[embedding],
                ids=[item_id],
                metadatas=[{"file_path": img_path}]
            )
        print(f"Indexed {len(image_files)} product images.")

    def find_similar_styles(self, query_image_path, n_results=5):
        """
        Input a custom image (e.g., a customer's inspiration photo) 
        and find the closest Schumacher products.
        """
        query_embedding = self.encode_image(query_image_path)
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        return results