import pandas as pd, aiohttp, asyncio
from pathlib import Path
from src.scrapers.lever_scraper import scrape as lever
from src.scrapers.greenhouse_scraper import scrape as greenhouse

BASE_DIR = Path(__file__).resolve().parents[2]
REGISTRY = BASE_DIR / "src/registry/company_registry.csv"
OUT = BASE_DIR / "data/raw/jobs_raw.csv"

SCRAPERS = {
    "lever": lever,
    "greenhouse": greenhouse
}

async def run():
    df = pd.read_csv(REGISTRY)
    all_rows = []

    async with aiohttp.ClientSession() as session:
        for _, row in df.iterrows():
            try:
                raw = await SCRAPERS[row.ats](session, row.company)
            except Exception as e:
                print(f"SKIP {row.company} ({row.ats}) → {e}")
                continue

            if row.ats == "greenhouse":
                raw = raw.get("jobs", [])

            for j in raw:
                if row.ats == "lever":
                    title = j.get("text")
                    url = j.get("hostedUrl")
                    location = j.get("categories",{}).get("location")
                else:
                    title = j.get("title")
                    url = j.get("absolute_url")
                    location = j.get("location",{}).get("name")

                all_rows.append({
                    "job_id": f"{row.ats}_{j.get('id')}",
                    "company": row.company,
                    "title": title,
                    "location": location,
                    "url": url,
                    "source": row.ats
                })

    pd.DataFrame(all_rows).to_csv(OUT, index=False)

asyncio.run(run())
