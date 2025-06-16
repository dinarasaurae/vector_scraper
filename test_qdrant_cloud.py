from qdrant_client import QdrantClient
from qdrant_client.http import models

API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.ASXWs6sd7NKNszZIy8n4Pj8VVOArWnBbcI6KPdyDczY"

client = QdrantClient(
    url="https://1feaa1ed-b77a-4c5d-80ea-d88a82ed2f56.eu-west-2-0.aws.cloud.qdrant.io",
    api_key=API_KEY,
)

print("Testing connection to Qdrant cloud")
try:
    collections = client.get_collections()
    print(f"Connection successful")
    print(f"Collections: {collections}")
    
    collection_name = "test_collection"
    collection_names = [c.name for c in collections.collections]
    
    if collection_name in collection_names:
        print(f"Collection '{collection_name}' already exists")
    else:
        print(f"Creating test collection '{collection_name}'...")
        
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=768,  
                distance=models.Distance.COSINE,
            ),
        )
        print(f"Collection '{collection_name}' created successfully")
    
    print("Testing point insertion...")
    client.upsert(
        collection_name=collection_name,
        points=[
            models.PointStruct(
                id=1,  
                vector=[0.1] * 768,  
                payload={"description": "This is a test point"}
            )
        ]
    )
    print("Point inserted successfully")
    
    print("Testing search")
    search_result = client.search(
        collection_name=collection_name,
        query_vector=[0.1] * 768,
        limit=1
    )
    print(f"Search successful! Results: {search_result}")
    
    print("\nQdrant cloud connection is working properly")
    
except Exception as e:
    print(f"Error connecting to Qdrant cloud: {e}")