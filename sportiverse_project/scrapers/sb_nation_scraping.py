import time
import random
import requests
import pandas as pd
from bs4 import BeautifulSoup

def scrape_sb_nation_articles():
    url= "https://www.sbnation.com"
    sb_nation_articles = []

    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve page, status code: {response.status_code}")
        return pd.DataFrame()

    soup = BeautifulSoup(response.content, "html.parser")

    river = soup.find("div", class_="c-compact-river")
    entries = river.find_all("div", class_="c-compact-river__entry") if river else []

    for entry in entries:
        body = entry.find("div", class_="c-entry-box--compact__body")
        if not body:
            continue

        title_tag = body.find("h2", class_="c-entry-box--compact__title")
        title = title_tag.get_text(strip=True) if title_tag else None
        link = title_tag.find("a")["href"] if title_tag and title_tag.find("a") else "Unknown"

        byline = body.find("div", class_="c-byline")
        author_tags = byline.find_all("span", class_="c-byline__author-name") if byline else []
        authors = ", ".join([tag.get_text(strip=True) for tag in author_tags]) if author_tags else "Unknown"

        time_tag = byline.find("time") if byline else None
        date = time_tag.get_text(strip=True) if time_tag else "Unknown"

        article_data = {
            'TITLE': title,
            'AUTHOR': authors,
            'DATE PUBLISHED': date,
            'ARTICLE LINK': link 
        }
        
        sb_nation_articles.append(article_data)

        time.sleep(random.uniform(1, 3))

    return pd.DataFrame(sb_nation_articles)