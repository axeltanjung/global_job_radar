from bs4 import BeautifulSoup
import re

def extract_company_links(html):
    soup = BeautifulSoup(html, "html.parser")
    links = set()

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("http") and not any(x in href for x in ["ycombinator","forbes","eu-startups"]):
            links.add(href.split("#")[0])
    return list(links)
