import os
from dotenv import load_dotenv

load_dotenv()

FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY", "fc-XXXXXXXx")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "XXXXXX")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "gemini")  # Options: gemini, openai, huggingface
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
HUGGINGFACE_MODEL = os.getenv("HUGGINGFACE_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

QDRANT_URL = os.getenv("QDRANT_URL", "https://XXXXXXXX")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "web_content")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "XXXXXXXXXXXX")

MAX_CHUNK_SIZE = int(os.getenv("MAX_CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "100"))
CHUNKING_STRATEGY = os.getenv("CHUNKING_STRATEGY", "paragraph")  # paragraph, sentence, token
