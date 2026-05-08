import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json
import os

# --- CONFIGURATION ---
# The AI will look for these topics to build your games
SEARCH_QUERY = "javascript physics engine game tutorial code snippets"
START_URLS = [
    "https://developer.mozilla.org/en-US/docs/Games/Tutorials/2D_Breakout_game_pure_JavaScript",
    "https://en.wikipedia.org/wiki/Physics_engine",
    "https://raw.githubusercontent.com/terrylow/PhysicsJS/master/dist/physicsjs.js"
]

async def fetch_and_analyze(session, url):
    try:
        async with session.get(url, timeout=10) as response:
            if response.status == 200:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Clean up the noise
                for s in soup(['script', 'style', 'nav', 'footer']):
                    s.decompose()
                
                text = soup.get_text()
                # Just grab the first 2000 characters to keep the file small
                return {"url": url, "data": text[:2000].strip()}
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

async def main():
    print("🚀 GENIE STARTING RESEARCH...")
    
    # Load existing brain or start fresh
    if os.path.exists('ai_brain.json'):
        with open('ai_brain.json', 'r') as f:
            try:
                brain_data = json.load(f)
            except:
                brain_data = []
    else:
        brain_data = []

    async with aiohttp.ClientSession(headers={'User-Agent': 'GenieBot/1.0'}) as session:
        tasks = [fetch_and_analyze(session, url) for url in START_URLS]
        new_knowledge = await asyncio.gather(*tasks)
        
        # Filter out failed attempts and add to brain
        for info in new_knowledge:
            if info and info not in brain_data:
                brain_data.append(info)

    # Save updated brain
    with open('ai_brain.json', 'w') as f:
        json.dump(brain_data, f, indent=4)
    
    print(f"✅ RESEARCH COMPLETE. {len(brain_data)} entries in memory.")

if __name__ == "__main__":
    asyncio.run(main())
