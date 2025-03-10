import os
import datetime
import time
from firecrawl import FirecrawlApp
import json
import anthropic
from dotenv import load_dotenv

load_dotenv()

anthropic_api_key = os.getenv("ANTHROPIC_API_KEY") or ""
firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY") or ""
blog_url="https://mendable.ai/blog"

client = anthropic.Anthropic(
    api_key=anthropic_api_key,
)

app = FirecrawlApp(api_key=firecrawl_api_key)

params = {
    'crawlOptions': {
        'limit': 100
    },
    "pageOptions": {
        "onlyMainContent": True
    }
}
crawl_result = app.crawl_url(blog_url, params=params)

potential_links = []

if crawl_result:
    print("Collecting potential links from crawl_result:")
    
    for item in crawl_result:
        metadata = item["metadata"]
        og_url = metadata.get("ogUrl")
        title = metadata.get("title")
        if og_url and title and og_url != blog_url:
            potential_links.append({"url": og_url, "title": title})
    
    print(f"Collected {len(potential_links)} potential links:")
    for link in potential_links:
        print(f"URL: {link['url']}, Title: {link['title']}")
else:
    print("crawl_result is empty or None")
