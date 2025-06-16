from typing import List, Dict, Any, Optional, Union
import datetime

from app.scraper.firecrawl import FirecrawlProvider
from app.processing.chunker import TextChunker
from app.processing.embeddings import get_embedding_provider
from app.storage.qdrant_client import QdrantStorage


class KnowledgeBase:
    def __init__(self):
        """Initialize the knowledge base components."""
        self.scraper = FirecrawlProvider()
        self.chunker = TextChunker()
        self.embedder = get_embedding_provider()
        self.storage = QdrantStorage()
    
    def process_website(
        self, 
        url: str, 
        depth: int = 1, 
        parse_js: bool = False,
        chunking_strategy: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process a website by scraping, chunking, embedding, and storing.
        
        Args:
            url: Website URL to process
            depth: Crawling depth
            parse_js: Whether to parse JavaScript
            chunking_strategy: Override default chunking strategy if provided
            
        Returns:
            Dictionary with processing stats
        """
        if chunking_strategy:
            valid_strategies = ['paragraph', 'sentence', 'token']
            strategy = str(chunking_strategy).lower().strip()
            
            if strategy in valid_strategies:
                self.chunker.strategy = strategy
            else:
                print(f"Warning: Invalid chunking strategy '{chunking_strategy}'. Using default strategy '{self.chunker.strategy}'.")
        
        scraped_pages = self.scraper.scrape(url, depth, parse_js)
        
        total_chunks = 0
        stored_ids = []
        
        for page in scraped_pages:
            page_url = page.get("url", url)
            chunks = self.chunker.chunk_text(
                page.get("text", ""),
                metadata={
                    "url": page_url,
                    "source": "web",
                    "timestamp": datetime.datetime.now().isoformat()
                }
            )
            
            if not chunks:
                continue
                
            texts = [chunk["text"] for chunk in chunks]
            embeddings = self.embedder.get_embeddings(texts)
            chunk_ids = self.storage.store_embeddings(chunks, embeddings)
            stored_ids.extend(chunk_ids)
            total_chunks += len(chunks)
        
        return {
            "url": url,
            "pages_processed": len(scraped_pages),
            "chunks_created": total_chunks,
            "vectors_stored": len(stored_ids)
        }
    
    def search(self, query: str, limit: int = 5, url_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        query_embedding = self.embedder.get_embeddings([query])[0]
        
        results = self.storage.search(
            query_vector=query_embedding,
            limit=limit,
            url_filter=url_filter
        )
        
        return results
    
    def delete_website(self, url: str) -> Dict[str, Any]:
        deleted_count = self.storage.delete_by_url(url)
        
        return {
            "url": url,
            "deleted_vectors": deleted_count
        }