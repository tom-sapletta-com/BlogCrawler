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
   git clone https://github.com/yourusername/blog-crawler.git
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

By default, the script will crawl "https://tom.sapletta.com/blog".

### Command Line Arguments

You can specify URLs to crawl in several ways:

1. Single URL:
   ```
   python crawler.py --url https://tom.sapletta.com/blog
   ```

2. Multiple URLs from a file (one URL per line):
   ```
   python crawler.py --file urls.txt
   ```

3. Extract URLs from a sitemap:
   ```
   python crawler.py --sitemap https://tom.sapletta.com/sitemap.xml
   ```
   
   With filtering (only crawl URLs containing a specific string):
   ```
   python crawler.py --sitemap https://tom.sapletta.com/sitemap.xml --filter blog
   ```

4. Explicitly use the default URL:
   ```
   python crawler.py --default
   ```

### Command Line Options

- `--url`: Specify a single blog URL to crawl
- `--file`: Specify a file containing multiple URLs to crawl (one URL per line)
- `--sitemap`: Specify a sitemap URL to extract URLs from
- `--filter`: Filter URLs from sitemap to only include those containing this string
- `--default`: Use the default URL (https://tom.sapletta.com/blog)

**Note:** The `--url`, `--file`, and `--sitemap` options are mutually exclusive. If none is specified, the default URL will be used automatically.
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
URL: https://tom.sapletta.com/blog/post1, Title: Example Post 1
URL: https://tom.sapletta.com/blog/post2, Title: Example Post 2
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
