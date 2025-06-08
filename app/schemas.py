from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class ScrapeRequest(BaseModel):
    url: HttpUrl

class PageData(BaseModel):
    url: HttpUrl
    text: str

class ScrapeResponse(BaseModel):
    status: str
    data: List[PageData]
