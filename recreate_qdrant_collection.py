from qdrant_client import QdrantClient
from qdrant_client.http import models
from app.config import QDRANT_URL, QDRANT_PORT, QDRANT_API_KEY, QDRANT_COLLECTION_NAME


client = QdrantClient(
    url=QDRANT_URL,
    port=QDRANT_PORT if QDRANT_URL == "localhost" else None,
    api_key=QDRANT_API_KEY,
    timeout=10
)

collections = client.get_collections().collections
collection_names = [c.name for c in collections]

if QDRANT_COLLECTION_NAME in collection_names:
    print(f"Deleting existing collection '{QDRANT_COLLECTION_NAME}'...")
    client.delete_collection(collection_name=QDRANT_COLLECTION_NAME)
    print(f"Collection '{QDRANT_COLLECTION_NAME}' deleted.")

print(f"Creating collection '{QDRANT_COLLECTION_NAME}'")
client.create_collection(
    collection_name=QDRANT_COLLECTION_NAME,
    vectors_config=models.VectorParams(
        size=768,
        distance=models.Distance.COSINE,
    ),
)

client.create_payload_index(
    collection_name=QDRANT_COLLECTION_NAME,
    field_name="url",
    field_schema="keyword"
)

print(f"Collection '{QDRANT_COLLECTION_NAME}' created successfully with 768 dimensions")