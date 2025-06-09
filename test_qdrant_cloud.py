from qdrant_client import QdrantClient
from qdrant_client.http import models

# Replace with your actual API key
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.ASXWs6sd7NKNszZIy8n4Pj8VVOArWnBbcI6KPdyDczY"

# Connect to your cloud instance
client = QdrantClient(
    url="https://1feaa1ed-b77a-4c5d-80ea-d88a82ed2f56.eu-west-2-0.aws.cloud.qdrant.io",
    api_key=API_KEY,
)

# Test the connection by listing collections
print("Testing connection to Qdrant cloud...")
try:
    collections = client.get_collections()
    print(f"✅ Connection successful!")
    print(f"Collections: {collections}")
    
    # Check if a test collection exists, or create it
    collection_name = "test_collection"
    collection_names = [c.name for c in collections.collections]
    
    if collection_name in collection_names:
        print(f"Collection '{collection_name}' already exists")
    else:
        print(f"Creating test collection '{collection_name}'...")
        
        # Create the collection with 768-dimension vectors (common for embedding models)
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=768,  # 768 dimensions
                distance=models.Distance.COSINE,
            ),
        )
        print(f"✅ Collection '{collection_name}' created successfully!")
    
    # Test inserting a point
    print("Testing point insertion...")
    client.upsert(
        collection_name=collection_name,
        points=[
            models.PointStruct(
                id=1,  # Use a numeric ID instead of a string
                vector=[0.1] * 768,  # Create a vector with all 0.1 values
                payload={"description": "This is a test point"}
            )
        ]
    )
    print("Point inserted successfully!")
    
    # Test searching
    print("Testing search...")
    search_result = client.search(
        collection_name=collection_name,
        query_vector=[0.1] * 768,
        limit=1
    )
    print(f"✅ Search successful! Results: {search_result}")
    
    print("\n✅ All tests passed! Your Qdrant cloud connection is working properly.")
    
except Exception as e:
    print(f"❌ Error connecting to Qdrant cloud: {e}")