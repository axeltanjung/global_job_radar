from src.utils.http import fetch_json
from src.config.ats_endpoints import ATS_ENDPOINTS

async def scrape(session, company):
    url = ATS_ENDPOINTS["greenhouse"].format(company=company)
    return await fetch_json(session, url)
