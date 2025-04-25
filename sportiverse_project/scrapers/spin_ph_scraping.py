import time
import random
import requests
import pandas as pd
from bs4 import BeautifulSoup

def scrape_spin_ph_articles(url="https://www.spin.ph/news/"):
    spin_ph_articles = []
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve page, status code: {response.status_code}")
        return pd.DataFrame()

    soup = BeautifulSoup(response.content, 'html.parser')
    cards = soup.find_all('div', class_='card')[:20] 

    for idx, card in enumerate(cards, start=1):
        try:
            a_tag_title_link = card.select_one('div.ttle a')
            link = a_tag_title_link['href']
            title = a_tag_title_link.get_text()

            a_tag_author = card.select_one('div.byln a')
            author = a_tag_author.get_text() if a_tag_author else "Unknown"

            data_published = card.select('div.stmp')
            date = None
            for tag in data_published:
                text = tag.get_text()
                if text:
                    date = text
                    break

            article_link = "https://www.spin.ph" + link
            article_data = {
                'TITLE': title,
                'AUTHOR': author,
                'DATE PUBLISHED': date,
                'ARTICLE LINK': article_link 
            }

            spin_ph_articles.append(article_data)
        except Exception as e:
            print(f"[{idx}] Error parsing article: {e}")

        time.sleep(random.uniform(1, 3))

    return pd.DataFrame(spin_ph_articles)
