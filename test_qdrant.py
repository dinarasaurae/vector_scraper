import sys
from app.config import QDRANT_URL, QDRANT_PORT, QDRANT_API_KEY, QDRANT_COLLECTION_NAME
from qdrant_client import QdrantClient
from qdrant_client.http import models

def test_qdrant_connection():
    print(f"Connecting to Qdrant at: {QDRANT_URL}:{QDRANT_PORT}")
    print(f"Using API key: {QDRANT_API_KEY[:10]}...")
    
    try:
        client = QdrantClient(
            url=QDRANT_URL,
            port=QDRANT_PORT,
            api_key=QDRANT_API_KEY,
            timeout=10
        )
        
        collections = client.get_collections()
        print(f"Connection successful! Collections: {collections}")
        
        collection_names = [c.name for c in collections.collections]
        if QDRANT_COLLECTION_NAME in collection_names:
            print(f"Collection '{QDRANT_COLLECTION_NAME}' exists!")
        else:
            print(f"Collection '{QDRANT_COLLECTION_NAME}' doesn't exist yet.")
            
            print(f"Creating collection '{QDRANT_COLLECTION_NAME}'...")
            
            vector_size = 768  
            
            client.create_collection(
                collection_name=QDRANT_COLLECTION_NAME,
                vectors_config=models.VectorParams(
                    size=vector_size,
                    distance=models.Distance.COSINE,
                ),
            )
            print(f"Collection '{QDRANT_COLLECTION_NAME}' created successfully")
            
        return True
    
    except Exception as e:
        print(f"Error connecting to Qdrant: {e}")
        return False

if __name__ == "__main__":
    success = test_qdrant_connection()
    sys.exit(0 if success else 1)