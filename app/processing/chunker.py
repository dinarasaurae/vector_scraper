"""
Text chunking module for splitting scraped content into manageable pieces.
"""
import re
from typing import List, Dict, Any, Optional
import tiktoken
from app.config import MAX_CHUNK_SIZE, CHUNK_OVERLAP, CHUNKING_STRATEGY


class TextChunker:
    """
    Splits text into smaller chunks based on different strategies.
    """
    
    def __init__(self, 
                 max_chunk_size: int = MAX_CHUNK_SIZE, 
                 chunk_overlap: int = CHUNK_OVERLAP,
                 strategy: str = CHUNKING_STRATEGY):
        """
        Initialize the text chunker.
        
        Args:
            max_chunk_size: Maximum size of each chunk in tokens or characters
            chunk_overlap: Number of tokens or characters to overlap between chunks
            strategy: Chunking strategy ('paragraph', 'sentence', or 'token')
        """
        self.max_chunk_size = max_chunk_size
        self.chunk_overlap = chunk_overlap
        self._tokenizer = None
        self._strategy = None
        # This will call the setter method which initializes tokenizer if needed
        self.strategy = strategy
        
    @property
    def strategy(self):
        """Get the current chunking strategy."""
        return self._strategy
        
    @strategy.setter
    def strategy(self, value):
        """
        Set the chunking strategy and initialize tokenizer if needed.
        
        Args:
            value: Chunking strategy ('paragraph', 'sentence', or 'token')
        """
        self._strategy = value
        
        # Initialize tokenizer for token counting if needed
        if value == 'token':
            self._tokenizer = tiktoken.get_encoding("cl100k_base")
            
    @property
    def tokenizer(self):
        """
        Get the tokenizer, initializing it if it doesn't exist.
        
        Returns:
            Tokenizer instance
        """
        if self._tokenizer is None and self.strategy == 'token':
            self._tokenizer = tiktoken.get_encoding("cl100k_base")
        return self._tokenizer
    
    def chunk_text(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Split text into chunks based on the selected strategy.
        
        Args:
            text: The text to chunk
            metadata: Optional metadata to include with each chunk
            
        Returns:
            List of dictionaries containing chunks and their metadata
        """
        if not text:
            return []
            
        chunks = []
        
        # Normalize strategy to lowercase and handle potential string input issues
        strategy = str(self.strategy).lower().strip()
        
        if strategy == 'paragraph':
            text_chunks = self._chunk_by_paragraph(text)
        elif strategy == 'sentence':
            text_chunks = self._chunk_by_sentence(text)
        elif strategy == 'token':
            text_chunks = self._chunk_by_token(text)
        else:
            # Default to paragraph if strategy is invalid
            print(f"Warning: Unknown chunking strategy: '{self.strategy}'. Using 'paragraph' instead.")
            text_chunks = self._chunk_by_paragraph(text)
        
        # Create chunk objects with metadata
        base_metadata = metadata or {}
        for i, chunk_text in enumerate(text_chunks):
            chunk = {
                "text": chunk_text,
                "chunk_index": i,
                **base_metadata
            }
            chunks.append(chunk)
            
        return chunks
    
    def _chunk_by_paragraph(self, text: str) -> List[str]:
        """Split text by paragraphs and combine until max chunk size is reached."""
        paragraphs = re.split(r'\n\s*\n|\r\n\s*\r\n', text)
        return self._combine_chunks(paragraphs)
    
    def _chunk_by_sentence(self, text: str) -> List[str]:
        """Split text by sentences and combine until max chunk size is reached."""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return self._combine_chunks(sentences)
    
    def _chunk_by_token(self, text: str) -> List[str]:
        """Split text by tokens and combine until max chunk size is reached."""
        tokens = self.tokenizer.encode(text)
        chunks = []
        
        i = 0
        while i < len(tokens):
            # Take a chunk of max_chunk_size
            chunk_end = min(i + self.max_chunk_size, len(tokens))
            chunk_tokens = tokens[i:chunk_end]
            chunks.append(self.tokenizer.decode(chunk_tokens))
            
            # Move forward by max_chunk_size - chunk_overlap
            i += self.max_chunk_size - self.chunk_overlap
            
        return chunks
    
    def _combine_chunks(self, elements: List[str]) -> List[str]:
        """Combine elements into chunks respecting max_chunk_size."""
        if self.strategy == 'token':
            return self._combine_chunks_by_tokens(elements)
        else:
            return self._combine_chunks_by_chars(elements)
    
    def _combine_chunks_by_chars(self, elements: List[str]) -> List[str]:
        """Combine elements into chunks based on character count."""
        chunks = []
        current_chunk = []
        current_size = 0
        
        for element in elements:
            element_size = len(element)
            
            if current_size + element_size <= self.max_chunk_size:
                current_chunk.append(element)
                current_size += element_size
            else:
                if current_chunk:
                    chunks.append("\n\n".join(current_chunk))
                current_chunk = [element]
                current_size = element_size
                
        if current_chunk:
            chunks.append("\n\n".join(current_chunk))
            
        return chunks
    
    def _combine_chunks_by_tokens(self, elements: List[str]) -> List[str]:
        """Combine elements into chunks based on token count."""
        chunks = []
        current_chunk = []
        current_size = 0
        
        for element in elements:
            element_size = len(self.tokenizer.encode(element))
            
            if current_size + element_size <= self.max_chunk_size:
                current_chunk.append(element)
                current_size += element_size
            else:
                if current_chunk:
                    chunks.append("\n\n".join(current_chunk))
                current_chunk = [element]
                current_size = element_size
                
        if current_chunk:
            chunks.append("\n\n".join(current_chunk))
            
        return chunks