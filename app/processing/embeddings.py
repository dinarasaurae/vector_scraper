"""
Embeddings module for generating vector representations of text.
"""
from typing import List, Dict, Any, Union
import numpy as np
import json
import requests
from abc import ABC, abstractmethod

from app.config import (
    EMBEDDING_PROVIDER, 
    OPENAI_API_KEY, 
    OPENAI_EMBEDDING_MODEL,
    HUGGINGFACE_MODEL,
    GEMINI_API_KEY
)


class EmbeddingProvider(ABC):
    """Base class for embedding providers."""
    
    @abstractmethod
    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            List of embedding vectors (as lists of floats)
        """
        pass


class OpenAIEmbeddings(EmbeddingProvider):
    """OpenAI embeddings provider."""
    
    def __init__(self, api_key: str = OPENAI_API_KEY, model: str = OPENAI_EMBEDDING_MODEL):
        """
        Initialize OpenAI embeddings provider.
        
        Args:
            api_key: OpenAI API key
            model: OpenAI embedding model name
        """
        self.api_key = api_key
        self.model = model
        
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=api_key)
        except ImportError:
            raise ImportError("OpenAI package not installed. Please install with: pip install openai")
    
    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings using OpenAI API."""
        if not texts:
            return []
            
        # Process in batches of 100 to avoid API limits
        batch_size = 100
        all_embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i+batch_size]
            
            response = self.client.embeddings.create(
                model=self.model,
                input=batch_texts
            )
            
            batch_embeddings = [item.embedding for item in response.data]
            all_embeddings.extend(batch_embeddings)
            
        return all_embeddings


class GeminiEmbeddings(EmbeddingProvider):
    """Google Gemini embeddings provider."""
    
    def __init__(self, api_key: str = GEMINI_API_KEY, model: str = "embedding-001"):
        """
        Initialize Gemini embeddings provider.
        
        Args:
            api_key: Gemini API key
            model: Gemini embedding model name
        """
        self.api_key = api_key
        self.model = model
        
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            self.genai = genai
        except ImportError:
            raise ImportError("Google Generative AI package not installed. " 
                              "Please install with: pip install google-generativeai")
        
    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings using Gemini API."""
        if not texts:
            return []
            
        # Process in batches of 100 to avoid API limits
        batch_size = 100
        all_embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i+batch_size]
            
            for text in batch_texts:
                try:
                    result = self.genai.embed_content(
                        model=self.model,
                        content=text,
                        task_type="retrieval_document"
                    )
                    all_embeddings.append(result["embedding"])
                except Exception as e:
                    error_message = f"Error from Gemini API: {str(e)}"
                    raise ValueError(error_message)
            
        return all_embeddings


class HuggingFaceEmbeddings(EmbeddingProvider):
    """HuggingFace Sentence Transformers embedding provider."""
    
    def __init__(self, model_name: str = HUGGINGFACE_MODEL):
        """
        Initialize HuggingFace embeddings provider.
        
        Args:
            model_name: HuggingFace model name or path
        """
        self.model_name = model_name
        
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(model_name)
        except ImportError:
            raise ImportError("Sentence-transformers package not installed. "
                             "Please install with: pip install sentence-transformers")
    
    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings using HuggingFace model."""
        if not texts:
            return []
            
        embeddings = self.model.encode(texts)
        return embeddings.tolist()


def get_embedding_provider() -> EmbeddingProvider:
    """
    Factory function to get the configured embedding provider.
    
    Returns:
        An instance of EmbeddingProvider based on configuration
    """
    if EMBEDDING_PROVIDER.lower() == "openai":
        return OpenAIEmbeddings()
    elif EMBEDDING_PROVIDER.lower() == "gemini":
        return GeminiEmbeddings()
    elif EMBEDDING_PROVIDER.lower() == "huggingface":
        return HuggingFaceEmbeddings()
    else:
        raise ValueError(f"Unknown embedding provider: {EMBEDDING_PROVIDER}")