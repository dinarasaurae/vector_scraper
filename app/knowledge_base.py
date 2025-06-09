"""
Knowledge base module that combines scraping, chunking, embedding, and vector storage.
"""
from typing import List, Dict, Any, Optional, Union
import datetime

from app.scraper.firecrawl import FirecrawlProvider
from app.processing.chunker import TextChunker
from app.processing.embeddings import get_embedding_provider
from app.storage.qdrant_client import QdrantStorage


class KnowledgeBase:
    """
    Knowledge base that scrapes websites, processes content, and stores vectors for searching.
    """
    
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
        # Override chunking strategy if provided
        if chunking_strategy:
            # Validate chunking strategy
            valid_strategies = ['paragraph', 'sentence', 'token']
            strategy = str(chunking_strategy).lower().strip()
            
            if strategy in valid_strategies:
                self.chunker.strategy = strategy
            else:
                print(f"Warning: Invalid chunking strategy '{chunking_strategy}'. Using default strategy '{self.chunker.strategy}'.")
        
        # Step 1: Scrape the website
        scraped_pages = self.scraper.scrape(url, depth, parse_js)
        
        total_chunks = 0
        stored_ids = []
        
        # Process each page
        for page in scraped_pages:
            page_url = page.get("url", url)
            
            # Step 2: Chunk the text
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
                
            # Step 3: Generate embeddings
            texts = [chunk["text"] for chunk in chunks]
            embeddings = self.embedder.get_embeddings(texts)
            
            # Step 4: Store in vector database
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
        """
        Search for content related to the query.
        
        Args:
            query: Search query text
            limit: Maximum number of results to return
            url_filter: Optional URL to filter results by
            
        Returns:
            List of search results with content and metadata
        """
        # Generate embedding for the query
        query_embedding = self.embedder.get_embeddings([query])[0]
        
        # Search in the vector database
        results = self.storage.search(
            query_vector=query_embedding,
            limit=limit,
            url_filter=url_filter
        )
        
        return results
    
    def delete_website(self, url: str) -> Dict[str, Any]:
        """
        Delete all content related to a specific website.
        
        Args:
            url: Website URL to delete
            
        Returns:
            Dictionary with deletion stats
        """
        deleted_count = self.storage.delete_by_url(url)
        
        return {
            "url": url,
            "deleted_vectors": deleted_count
        }