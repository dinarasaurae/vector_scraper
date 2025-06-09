import requests
import logging

class FirecrawlProvider:
    FIRECRAWL_API = "https://api.firecrawl.dev/v1/scrape"

    def scrape(self, url, depth=1, parse_js=False):
        """
        For testing with Qdrant cloud, we'll use a mock response
        instead of calling the actual API
        """
        print(f"Mock scraping {url}...")
        
        # Return mock data for testing with Qdrant
        if "wikipedia" in url and "artificial_intelligence" in url:
            return [{
                "url": url,
                "text": """Artificial intelligence (AI) is intelligence demonstrated by machines, 
                unlike natural intelligence displayed by animals including humans. 
                AI research has been defined as the field of study of intelligent agents, 
                which refers to any system that perceives its environment and takes actions 
                that maximize its chance of achieving its goals.
                
                The term "artificial intelligence" had previously been used to describe machines 
                that mimic and display "human" cognitive skills that are associated with the human mind, 
                such as "learning" and "problem-solving". This definition has since been rejected 
                by major AI researchers who now describe AI in terms of rationality and acting rationally, 
                which does not limit how intelligence can be articulated.
                
                AI applications include advanced web search engines (e.g., Google), recommendation systems 
                (used by YouTube, Amazon, and Netflix), understanding human speech (such as Siri and Alexa), 
                self-driving cars (e.g., Waymo), generative or creative tools (ChatGPT and AI art), 
                automated decision-making, and competing at the highest level in strategic game systems.
                """
            }]
        else:
            return [{
                "url": url,
                "text": f"This is sample text for {url} used for testing purposes."
            }]
