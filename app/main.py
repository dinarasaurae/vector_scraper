from fastapi import FastAPI, HTTPException, Query
from typing import Optional, List

from app.schemas import (
    ScrapeRequest, 
    ScrapeResponse, 
    PageData, 
    ProcessWebsiteRequest, 
    ProcessWebsiteResponse,
    SearchRequest,
    SearchResponse,
    SearchResult
)
from app.scraper.firecrawl import FirecrawlProvider
from app.scraper.proprietary import OwnScraperProvider
from app.knowledge_base import KnowledgeBase

app = FastAPI(
    title="Scraper and Knowledge Base API",
    description="API for scraping websites and building a searchable knowledge base"
)

kb = KnowledgeBase()

def get_provider(source: str):
    if source == "firecrawl":
        return FirecrawlProvider()
    else:
        return OwnScraperProvider()

@app.post(
    "/api/scrape",
    response_model=ScrapeResponse,
    summary="Scrape a website",
    response_description="Content of website pages"
)
def scrape(payload: ScrapeRequest):
    provider = get_provider(payload.source)
    try:
        data = provider.scrape(
            url=str(payload.url),
            depth=payload.depth,
            parse_js=payload.parseJs
        )
        pages = [PageData(**page) for page in data]
        return ScrapeResponse(status="success", data=pages)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post(
    "/api/kb/process",
    response_model=ProcessWebsiteResponse,
    summary="Process a website into the knowledge base",
    response_description="Processing statistics"
)
def process_website(payload: ProcessWebsiteRequest):
    """
    Process a website by scraping, chunking, embedding, and storing in the vector database.
    """
    try:
        if payload.chunkingStrategy:
            valid_strategies = ['paragraph', 'sentence', 'token']
            if payload.chunkingStrategy.lower() not in valid_strategies:
                raise ValueError(f"Invalid chunking strategy: '{payload.chunkingStrategy}'. Must be one of: {', '.join(valid_strategies)}")
        
        result = kb.process_website(
            url=str(payload.url),
            depth=payload.depth,
            parse_js=payload.parseJs,
            chunking_strategy=payload.chunkingStrategy
        )
        return ProcessWebsiteResponse(status="success", data=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Error processing website: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post(
    "/api/kb/search",
    response_model=SearchResponse,
    summary="Search the knowledge base",
    response_description="Search results"
)
def search_kb(payload: SearchRequest):
    """
    Search the knowledge base for content related to the query.
    """
    try:
        results = kb.search(
            query=payload.query,
            limit=payload.limit,
            url_filter=payload.urlFilter
        )
        search_results = [SearchResult(**result) for result in results]
        return SearchResponse(status="success", data=search_results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete(
    "/api/kb/website",
    summary="Delete website data from the knowledge base",
    response_description="Deletion statistics"
)
def delete_website(url: str = Query(..., description="Website URL to delete")):
    """
    Delete all content related to a specific website from the knowledge base.
    """
    try:
        result = kb.delete_website(url)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
