import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# API Keys
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY", "fc-ee16373dcd7d4b3b909e59e190e6c837")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyCvbMXbRlXzbuP8io1jtSwZtAmmCCz9f3Q")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Embedding Configuration
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "gemini")  # Options: gemini, openai, huggingface
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
HUGGINGFACE_MODEL = os.getenv("HUGGINGFACE_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

# Qdrant Configuration
QDRANT_URL = os.getenv("QDRANT_URL", "https://1feaa1ed-b77a-4c5d-80ea-d88a82ed2f56.eu-west-2-0.aws.cloud.qdrant.io")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "web_content")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.ASXWs6sd7NKNszZIy8n4Pj8VVOArWnBbcI6KPdyDczY")

# Chunking Configuration
MAX_CHUNK_SIZE = int(os.getenv("MAX_CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "100"))
CHUNKING_STRATEGY = os.getenv("CHUNKING_STRATEGY", "paragraph")  # Options: paragraph, sentence, token
