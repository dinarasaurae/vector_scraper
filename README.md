# Web Scraping and Knowledge Base

This project provides a pipeline for:
1. Scraping websites using Firecrawl API
2. Processing and chunking the content
3. Generating embeddings for text chunks
4. Storing embeddings in Qdrant vector database
5. Searching for semantically similar content

## Features

- Website scraping using Firecrawl API
- Multiple text chunking strategies (paragraph, sentence, token)
- Support for different embedding providers (Google Gemini, OpenAI, HuggingFace)
- Vector storage and search with Qdrant
- FastAPI endpoints for processing websites and searching
- Command-line interface for easy testing

## Installation

1. Clone the repository
2. Install dependencies:
```
pip install -r requirements.txt
```

3. Create a `.env` file with your API keys (optional):
```
FIRECRAWL_API_KEY=your_firecrawl_key
GEMINI_API_KEY=your_gemini_key
OPENAI_API_KEY=your_openai_key
QDRANT_API_KEY=your_qdrant_key_if_using_cloud
```

## Usage

### API

Start the FastAPI server:
```
uvicorn app.main:app --reload
```

API endpoints:
- `POST /api/scrape` - Scrape a website
- `POST /api/kb/process` - Process a website into the knowledge base
- `POST /api/kb/search` - Search the knowledge base
- `DELETE /api/kb/website` - Delete website data from the knowledge base

### Command Line

The example.py script provides a command-line interface:

Process a website:
```
python example.py process https://example.com --depth 2
```

Search the knowledge base:
```
python example.py search "your search query" --limit 10
```

Delete website data:
```
python example.py delete https://example.com
```

## Architecture

The project consists of the following components:

1. **Scraper**: Uses Firecrawl API to extract content from websites
2. **Chunker**: Splits text into manageable chunks using different strategies
3. **Embedder**: Generates vector embeddings using OpenAI or HuggingFace models
4. **Storage**: Stores and searches vectors using Qdrant database
5. **Knowledge Base**: Orchestrates the entire pipeline

## Configuration

Configuration options are in `app/config.py` and can be overridden using environment variables:

- `FIRECRAWL_API_KEY`: API key for Firecrawl
- `GEMINI_API_KEY`: API key for Google Gemini (if using Gemini embeddings)
- `OPENAI_API_KEY`: API key for OpenAI (if using OpenAI embeddings)
- `EMBEDDING_PROVIDER`: Which embedding provider to use ('gemini', 'openai', or 'huggingface')
- `OPENAI_EMBEDDING_MODEL`: OpenAI embedding model to use
- `HUGGINGFACE_MODEL`: HuggingFace model to use
- `QDRANT_URL`: Qdrant server URL
- `QDRANT_PORT`: Qdrant server port
- `QDRANT_COLLECTION_NAME`: Qdrant collection name
- `QDRANT_API_KEY`: Qdrant API key (if using cloud)
- `MAX_CHUNK_SIZE`: Maximum size of text chunks
- `CHUNK_OVERLAP`: Overlap between chunks
- `CHUNKING_STRATEGY`: Default chunking strategy

## Tests

Run the tests:
```
pytest
```

## License

MIT