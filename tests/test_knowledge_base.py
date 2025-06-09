"""
Tests for the knowledge base functionality.
"""
import pytest
from unittest.mock import MagicMock, patch
from app.knowledge_base import KnowledgeBase
from app.processing.chunker import TextChunker
from app.processing.embeddings import OpenAIEmbeddings

# Sample test data
TEST_URL = "https://example.com"
TEST_TEXT = """
This is a sample text for testing.
It has multiple paragraphs.

This is the second paragraph with some content.
It should be chunked appropriately.

And here's a third paragraph with additional information.
"""

@pytest.fixture
def mocked_kb():
    """Create a knowledge base with mocked components."""
    kb = KnowledgeBase()
    
    # Mock the scraper
    kb.scraper = MagicMock()
    kb.scraper.scrape.return_value = [
        {"url": TEST_URL, "text": TEST_TEXT}
    ]
    
    # Use real chunker but mock embedder and storage
    kb.chunker = TextChunker(strategy="paragraph")
    kb.embedder = MagicMock()
    kb.embedder.get_embeddings.return_value = [[0.1, 0.2, 0.3]]
    
    kb.storage = MagicMock()
    kb.storage.store_embeddings.return_value = ["id1", "id2", "id3"]
    kb.storage.search.return_value = [
        {
            "id": "id1",
            "score": 0.95,
            "text": "Sample text chunk",
            "url": TEST_URL,
            "chunk_index": 0
        }
    ]
    
    return kb

def test_process_website(mocked_kb):
    """Test the website processing pipeline."""
    # Process a test website
    result = mocked_kb.process_website(TEST_URL)
    
    # Verify the scraper was called correctly
    mocked_kb.scraper.scrape.assert_called_once_with(TEST_URL, 1, False)
    
    # Verify chunks were created and processed
    assert mocked_kb.embedder.get_embeddings.called
    assert mocked_kb.storage.store_embeddings.called
    
    # Check the result contains expected keys
    assert "url" in result
    assert "pages_processed" in result
    assert "chunks_created" in result
    assert "vectors_stored" in result

def test_search(mocked_kb):
    """Test the search functionality."""
    # Search for a test query
    results = mocked_kb.search("test query")
    
    # Verify the embedding and search were performed
    assert mocked_kb.embedder.get_embeddings.called
    assert mocked_kb.storage.search.called
    
    # Check we got results back
    assert len(results) > 0
    assert "id" in results[0]
    assert "score" in results[0]
    assert "text" in results[0]

def test_chunker():
    """Test the text chunking functionality."""
    chunker = TextChunker(strategy="paragraph")
    chunks = chunker.chunk_text(TEST_TEXT, {"url": TEST_URL})
    
    # Check we got chunks back
    assert len(chunks) > 0
    assert "text" in chunks[0]
    assert "url" in chunks[0]
    assert "chunk_index" in chunks[0]