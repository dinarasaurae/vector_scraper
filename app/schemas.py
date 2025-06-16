from pydantic import BaseModel, HttpUrl, Field, validator
from typing import List, Optional, Dict, Any

class ScrapeRequest(BaseModel):
    url: HttpUrl
    depth: int = 1
    parseJs: bool = False
    source: str = "firecrawl"

class PageData(BaseModel):
    url: HttpUrl
    text: str

class ScrapeResponse(BaseModel):
    status: str
    data: List[PageData]

class ProcessWebsiteRequest(BaseModel):
    url: HttpUrl
    depth: int = 1
    parseJs: bool = False
    chunkingStrategy: Optional[str] = None
    
    @validator('chunkingStrategy')
    def validate_chunking_strategy(cls, v):
        if v is not None:
            valid_strategies = ['paragraph', 'sentence', 'token']
            strategy = str(v).lower().strip()
            if strategy not in valid_strategies:
                raise ValueError(f"Invalid chunking strategy: {v}. Must be one of: paragraph, sentence, token")
            return strategy
        return v
    
class ProcessWebsiteResponse(BaseModel):
    status: str
    data: Dict[str, Any]

class SearchRequest(BaseModel):
    query: str
    limit: int = 5
    urlFilter: Optional[str] = None
    
class SearchResult(BaseModel):
    id: str
    score: float
    text: str
    url: str
    chunk_index: int = 0
    title: Optional[str] = None
    source: str = "web"
    
class SearchResponse(BaseModel):
    status: str
    data: List[SearchResult]
