from typing import List, Dict, Any, Optional, Union
import uuid

from qdrant_client import QdrantClient
from qdrant_client.http.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
    SearchRequest
)

from app.config import (
    QDRANT_URL,
    QDRANT_PORT,
    QDRANT_COLLECTION_NAME,
    QDRANT_API_KEY,
    EMBEDDING_PROVIDER
)


class QdrantStorage:
    """Qdrant vector database storage for embeddings."""
    
    def __init__(
        self,
        url: str = QDRANT_URL,
        port: int = QDRANT_PORT,
        collection_name: str = QDRANT_COLLECTION_NAME,
        api_key: Optional[str] = QDRANT_API_KEY,
        vector_size: int = 768  # Gemini, у openai вроде другое
    ):
        """
        Initialize Qdrant storage.
        
        Args:
            url: Qdrant server URL
            port: Qdrant server port
            collection_name: Name of the collection to use
            api_key: Qdrant API key (if using cloud)
            vector_size: Size of embedding vectors
        """
        self.url = url
        self.port = port
        self.collection_name = collection_name
        self.api_key = api_key
        self.vector_size = vector_size
        
        client_kwargs = {
            "url": url, 
            "port": port if url == "localhost" else None
        }
        
        if api_key:
            client_kwargs["api_key"] = api_key
            
        self.client = QdrantClient(**client_kwargs)
        self._create_collection_if_not_exists()
    
    def _create_collection_if_not_exists(self):
        """Create the collection if it doesn't exist."""
        collections = self.client.get_collections().collections
        collection_names = [collection.name for collection in collections]
        
        if self.collection_name not in collection_names:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=self.vector_size, distance=Distance.COSINE)
            )
            
            self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name="url",
                field_schema="keyword"
            )
    
    def store_embeddings(self, chunks: List[Dict[str, Any]], embeddings: List[List[float]]) -> List[str]:
        """
        Store text chunks with their embeddings in Qdrant.
        
        Args:
            chunks: List of chunk dictionaries with text and metadata
            embeddings: List of embedding vectors corresponding to chunks
            
        Returns:
            List of point IDs stored in Qdrant
        """
        if len(chunks) != len(embeddings):
            raise ValueError("Number of chunks and embeddings must match")
            
        points = []
        point_ids = []
        
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            point_id = i + 1  
            point_ids.append(str(point_id))  
            
            points.append(
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload={
                        "text": chunk["text"],
                        "url": chunk.get("url", ""),
                        "chunk_index": chunk.get("chunk_index", i),
                        "source": chunk.get("source", "web"),
                        "title": chunk.get("title", ""),
                        "timestamp": chunk.get("timestamp", "")
                    }
                )
            )
        
        batch_size = 100
        for i in range(0, len(points), batch_size):
            batch = points[i:i+batch_size]
            self.client.upsert(
                collection_name=self.collection_name,
                points=batch
            )
            
        return point_ids
    
    def search(
        self, 
        query_vector: List[float],
        limit: int = 5,
        url_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar vectors in Qdrant.
        
        Args:
            query_vector: The query embedding vector
            limit: Maximum number of results to return
            url_filter: Optional URL to filter results by
            
        Returns:
            List of dictionaries containing search results with scores and payloads
        """
        search_filter = None
        if url_filter:
            search_filter = Filter(
                must=[
                    FieldCondition(
                        key="url",
                        match=MatchValue(value=url_filter)
                    )
                ]
            )
        
        search_results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit,
            query_filter=search_filter
        )
        
        results = []
        for result in search_results:
            results.append({
                "id": result.id,
                "score": result.score,
                "text": result.payload.get("text", ""),
                "url": result.payload.get("url", ""),
                "chunk_index": result.payload.get("chunk_index", 0),
                "title": result.payload.get("title", ""),
                "source": result.payload.get("source", "web")
            })
            
        return results
    
    def delete_by_url(self, url: str) -> int:
        """
        Delete all vectors associated with a specific URL.
        
        Args:
            url: The URL to delete vectors for
            
        Returns:
            Number of points deleted
        """
        try:
            count_result = self.client.count(
                collection_name=self.collection_name,
                count_filter=Filter(
                    must=[
                        FieldCondition(
                            key="url",
                            match=MatchValue(value=url)
                        )
                    ]
                )
            )
            points_to_delete = count_result.count
            
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=Filter(
                    must=[
                        FieldCondition(
                            key="url",
                            match=MatchValue(value=url)
                        )
                    ]
                )
            )
            return points_to_delete
        except Exception as e:
            print(f"Error deleting points: {e}")
            return 0