import requests
from bs4 import BeautifulSoup
from schemes.models import Scheme


def scrape_myscheme():
    url = "https://www.myscheme.gov.in"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Example scraping logic (simplified)
    for link in soup.find_all("a"):
        title = link.text.strip()
        href = link.get("href")

        if title and href and "scheme" in href:
            Scheme.objects.get_or_create(
                title=title,
                defaults={
                    "description": "Auto scraped from MyScheme portal",
                    "category": "employment",
                    "govt_type": "central",
                    "official_link": href
                }
            )
