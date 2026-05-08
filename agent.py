import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json
import datetime
import re

# Add the specific topics you want your Genie to master
TARGETS = [
    "https://developer.mozilla.org/en-US/docs/Games/Tutorials/2D_Breakout_game_pure_JavaScript",
    "https://web.dev/articles/canvas-basic-usage",
    "https://pothonprogramming.github.io/"
]

async def scrape(session, url):
    try:
        async with session.get(url, timeout=5) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            
            # Find the most relevant text (paragraphs)
            content = " ".join([p.text for p in soup.find_all('p')[:3]])
            # Clean up junk characters and extra spaces
            content = re.sub(r'\s+', ' ', content).strip()
            
            return {
                "url": url,
                "title": soup.title.string if soup.title else "Genie Resource",
                "data": content,
                "timestamp": datetime.datetime.now().strftime("%I:%M %p")
            }
    except:
        return None

async def main():
    async with aiohttp.ClientSession(headers={'User-Agent': 'Genie-Bot/1.0'}) as session:
        results = await asyncio.gather(*[scrape(session, u) for u in TARGETS])
        # Filter out failed sites
        clean_data = [r for r in results if r]
        
        with open('ai_brain.json', 'w') as f:
            json.dump(clean_data, f, indent=4)
        print(f"🚀 Genie synchronized {len(clean_data)} research nodes.")

if __name__ == "__main__":
    asyncio.run(main())
