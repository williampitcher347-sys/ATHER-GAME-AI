import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json
import datetime
import re

TARGETS = [
    # Core Interactive Learning Environments
    "https://code.org",
    "https://www.w3schools.com",
    "https://bencentra.com",
    
    # Engine Lifecycle Documentation & Sandboxes
    "https://developer.mozilla.org",
    "https://phaser.io",
    "https://playcanvas.com",
    
    # Mathematical & Computational Logic Sites
    "https://thecodingtrain.com",
    "https://natureofcode.com",
    
    # Micro-Project & Retro Coding Explanations
    "https://blogspot.com",
    "https://tutsplus.com",
    "https://williammalone.com" 
]

# Standard Chrome User-Agent header to avoid basic bot detection
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}

async def scrape(session, url):
    try:
        # Increased timeout to 10s for slower responding sites
        async with session.get(url, headers=HEADERS, timeout=10) as response:
            if response.status != 200:
                print(f"⚠️ Failed {url} with status {response.status}")
                return None

            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            
            # Find the most relevant text (paragraphs)
            paragraphs = soup.find_all('p')
            content = " ".join([p.get_text() for p in paragraphs[:3]])
            
            # Clean up junk characters and extra spaces
            content = re.sub(r'\s+', ' ', content).strip()
            
            title = soup.title.get_text().strip() if soup.title else "Genie Resource"
            
            # Skip Cloudflare challenge pages if caught
            if "Just a moment..." in title:
                print(f"🛡️ Blocked by Cloudflare: {url}")
                return None

            return {
                "url": url,
                "title": title,
                "data": content,
                "timestamp": datetime.datetime.now().strftime("%I:%M %p")
            }
    except Exception as e:
        print(f"❌ Error fetching {url}: {e}")
        return None

async def main():
    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(*[scrape(session, u) for u in TARGETS])
        
        # Filter out failed sites or blocked responses
        clean_data = [r for r in results if r]
        
        with open('ai_brain.json', 'w', encoding='utf-8') as f:
            json.dump(clean_data, f, indent=4)
            
        print(f"\n🚀 Genie successfully synchronized {len(clean_data)} research nodes to ai_brain.json!")

if __name__ == "__main__":
    asyncio.run(main())
