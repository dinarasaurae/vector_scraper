import requests
from app.config import FIRECRAWL_API_KEY

class FirecrawlProvider:
    FIRECRAWL_API = "https://api.firecrawl.dev/v1/scrape"

    def scrape(self, url, depth=1, parse_js=False):
        headers = {"Authorization": f"Bearer {FIRECRAWL_API_KEY}"}
        payload = {
            "url": url
        }
        resp = requests.post(self.FIRECRAWL_API, headers=headers, json=payload)
        resp.raise_for_status()  
        result = resp.json()
        return [
            {
                "url": page.get("url", url),
                "text": page.get("text", "")
            }
            for page in result.get("data", [])
        ]
