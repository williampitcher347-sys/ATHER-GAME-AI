import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json
import datetime

# The mission
SEARCH_QUERY = "javascript game physics engine tutorial"
URLS = [
    f"https://www.google.com/search?q={SEARCH_QUERY}",
    "https://developer.mozilla.org/en-US/docs/Games/Tutorials",
    "https://web.dev/learn/design/animations",
    "https://codepen.io/search/pens?q=game+physics"
]

async def scrape_site(session, url):
    try:
        async with session.get(url, timeout=10) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            # Extract only the important text
            text = ' '.join([p.text for p in soup.find_all('p')[:3]])
            return {"url": url, "data": text, "time": str(datetime.datetime.now())}
    except Exception as e:
        return None

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [scrape_site(session, url) for url in URLS]
        results = await asyncio.gather(*tasks)
        
        # Filter out failed searches and save
        clean_results = [r for r in results if r is not None]
        with open('ai_brain.json', 'w') as f:
            json.dump(clean_results, f, indent=4)
        print(f"Genie updated {len(clean_results)} sources.")

if __name__ == "__main__":
    asyncio.run(main())
