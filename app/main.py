from fastapi import FastAPI, HTTPException
from app.schemas import ScrapeRequest, ScrapeResponse, PageData
from app.scraper.firecrawl import FirecrawlProvider
from app.scraper.proprietary import OwnScraperProvider

app = FastAPI(
    title="Scraper Gateway API",
    description="API для скрейпинга сайтов через Firecrawl или свой движок"
)

def get_provider(source: str):
    if source == "firecrawl":
        return FirecrawlProvider()
    else:
        return OwnScraperProvider()

@app.post(
    "/api/scrape",
    response_model=ScrapeResponse,
    summary="Скрейпинг сайта",
    response_description="Контент страниц сайта"
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
