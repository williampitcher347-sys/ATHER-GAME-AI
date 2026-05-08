import asyncio
import aiohttp
import json

# Faster search logic
async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(fetch_site(session, url))
        return await asyncio.gather(*tasks) # This runs them all AT ONCE

async def fetch_site(session, url):
    try:
        async with session.get(url, timeout=5) as response:
            text = await response.text()
            # Tidy up the data immediately
            return {"url": url, "snippet": text[:1000].replace('\n', ' ')}
    except:
        return None
