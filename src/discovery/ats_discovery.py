import re, aiohttp, asyncio
from bs4 import BeautifulSoup
from urllib.parse import urlparse

ATS_PATTERNS = {
    "greenhouse": r"boards\.greenhouse\.io/([^/\"']+)",
    "lever": r"jobs\.lever\.co/([^/\"']+)",
    "workable": r"apply\.workable\.com/([^/\"']+)",
    "smartrecruiters": r"careers\.smartrecruiters\.com/([^/\"']+)",
    "ashby": r"jobs\.ashbyhq\.com/([^/\"']+)"
}

async def discover_from_homepage(session, homepage: str):
    try:
        async with session.get(homepage, timeout=20) as r:
            html = await r.text()
    except:
        return []

    found = set()

    for ats, pat in ATS_PATTERNS.items():
        for slug in re.findall(pat, html):
            found.add((slug.lower(), ats, homepage))

    return list(found)
