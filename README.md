# Blog Crawler

A Python utility for crawling blog content and extracting potential links using the Firecrawl and Anthropic APIs.

## Overview

This tool crawls a specified blog URL, extracts metadata from the pages, and collects links with their titles. It uses the Firecrawl API for web crawling capabilities and is set up to potentially use the Anthropic API for further processing (though the current implementation doesn't actively use Anthropic).

## Prerequisites

- Python 3.6+
- Firecrawl API key
- Anthropic API key (optional for the current implementation)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/tom-sapletta-com/BlogCrawler.git
   cd blog-crawler
   ```

2. Install the required dependencies:
   ```
   pip install anthropic python-dotenv firecrawl
   ```

3. Create a `.env` file in the root directory with your API keys:
   ```
   ANTHROPIC_API_KEY=your_anthropic_api_key
   FIRECRAWL_API_KEY=your_firecrawl_api_key
   ```

## Usage

Run the script directly:

```
python crawler.py
```

By default, the script will crawl the URL specified in the `blog_url` variable (currently set to "https://mendable.ai/blog").

### Customization

- Modify the `blog_url` variable to crawl a different blog
- Adjust the `params` dictionary to change crawling options:
  - `limit`: Maximum number of pages to crawl
  - `onlyMainContent`: Whether to extract only the main content of pages

## How It Works

1. The script loads environment variables from a `.env` file
2. It initializes the Firecrawl and Anthropic clients with API keys
3. It crawls the specified blog URL with the given parameters
4. For each item in the crawl results, it extracts:
   - The Open Graph URL (`ogUrl`)
   - The page title
5. It filters out items that don't have both URL and title, or where the URL matches the original blog URL
6. It prints the collected links and their titles to the console

## Example Output

```
Collecting potential links from crawl_result:
Collected 15 potential links:
URL: https://mendable.ai/blog/post1, Title: Example Post 1
URL: https://mendable.ai/blog/post2, Title: Example Post 2
...
```

## Configuration Options

### Crawl Options

```python
params = {
    'crawlOptions': {
        'limit': 100  # Maximum number of pages to crawl
    },
    "pageOptions": {
        "onlyMainContent": True  # Extract only main content
    }
}
```

## Error Handling

The script checks if `crawl_result` is empty or None and provides appropriate feedback.

