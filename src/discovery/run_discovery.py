import aiohttp, asyncio, csv, re

ATS_DOMAINS = {
    "greenhouse": r"https://boards\.greenhouse\.io/([^/\"']+)",
    "lever": r"https://jobs\.lever\.co/([^/\"']+)",
    "workable": r"https://apply\.workable\.com/([^/\"']+)",
    "smartrecruiters": r"https://careers\.smartrecruiters\.com/([^/\"']+)",
    "ashby": r"https://jobs\.ashbyhq\.com/([^/\"']+)"
}

async def harvest(domain, session):
    url = f"https://{domain}"
    try:
        async with session.get(url, timeout=20) as r:
            html = await r.text()
    except:
        return []

    found = []
    for ats, pat in ATS_DOMAINS.items():
        for slug in re.findall(pat, html):
            found.append((slug.lower(), ats))
    return found

async def run():
    seeds = open("src/discovery/seeds.txt").read().splitlines()
    registry = set()

    async with aiohttp.ClientSession() as session:
        for domain in seeds:
            results = await harvest(domain, session)
            for slug, ats in results:
                registry.add((slug, ats))

    with open("src/registry/company_registry.csv","a",newline="",encoding="utf8") as f:
        writer = csv.writer(f)
        for slug, ats in registry:
            writer.writerow([slug, ats, "UNKNOWN"])

asyncio.run(run())
