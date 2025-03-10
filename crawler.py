import os
import datetime
import time
import argparse
from firecrawl import FirecrawlApp
import json
import anthropic
from dotenv import load_dotenv

def crawl_url(app, url, params):
    """
    Crawl a single URL and extract potential links from it.
    
    Args:
        app: The FirecrawlApp instance
        url: The URL to crawl
        params: Crawling parameters
        
    Returns:
        list: A list of potential links
    """
    print(f"Crawling URL: {url}")
    crawl_result = app.crawl_url(url, params=params)
    
    potential_links = []
    
    if crawl_result:
        print("Collecting potential links from crawl_result:")
        
        for item in crawl_result:
            metadata = item["metadata"]
            og_url = metadata.get("ogUrl")
            title = metadata.get("title")
            if og_url and title and og_url != url:
                potential_links.append({"url": og_url, "title": title})
        
        print(f"Collected {len(potential_links)} potential links from {url}:")
        for link in potential_links:
            print(f"URL: {link['url']}, Title: {link['title']}")
    else:
        print(f"crawl_result for {url} is empty or None")
    
    return potential_links

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Crawl a blog and extract links.')
    url_group = parser.add_mutually_exclusive_group()
    url_group.add_argument('--url', type=str, 
                        help='URL of the blog to crawl')
    url_group.add_argument('--file', type=str,
                        help='Path to file containing URLs to crawl (one URL per line)')
    parser.add_argument('--default', action='store_true',
                        help='Use default URL (https://mendable.ai/blog) if no other source is specified')
    args = parser.parse_args()
    
    # Load environment variables
    load_dotenv()
    
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY") or ""
    firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY") or ""
    
    # Determine the URLs to crawl
    urls_to_crawl = []
    
    if args.url:
        urls_to_crawl = [args.url]
    elif args.file:
        try:
            with open(args.file, 'r') as file:
                urls_to_crawl = [line.strip() for line in file if line.strip()]
            print(f"Loaded {len(urls_to_crawl)} URLs from {args.file}")
        except Exception as e:
            print(f"Error reading URL file: {e}")
            return
    elif args.default or (not args.url and not args.file):
        urls_to_crawl = ["https://mendable.ai/blog"]
        print("Using default URL: https://mendable.ai/blog")
    
    if not urls_to_crawl:
        print("No URLs to crawl. Please specify a URL, a file, or use the default.")
        return
    
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
    
    # Store all collected links
    all_potential_links = []
    
    # Process each URL
    for url in urls_to_crawl:
        potential_links = crawl_url(app, url, params)
        all_potential_links.extend(potential_links)
        
        # Add a small delay between requests to be nice to the server
        if len(urls_to_crawl) > 1 and url != urls_to_crawl[-1]:
            print("Waiting 2 seconds before next request...")
            time.sleep(2)
    
    # Summary
    print("\nSummary:")
    print(f"Crawled {len(urls_to_crawl)} URLs")
    print(f"Collected a total of {len(all_potential_links)} potential links")

if __name__ == "__main__":
    main()
