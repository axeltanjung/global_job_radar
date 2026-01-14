import aiohttp

async def fetch_json(session: aiohttp.ClientSession, url: str):
    async with session.get(url, timeout=30) as r:
        r.raise_for_status()
        return await r.json()
