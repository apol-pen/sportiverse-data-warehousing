"""
scrape_sb_nation_articles.py

This script scrapes the latest articles from the SB Nation homepage.
It collects article titles, authors, publication dates, and article links,
and saves them into a pandas DataFrame.

Author: Karl Apolonio
Date: April 27, 2025

Modules used:
- time: For adding random sleep times between requests (be polite to server)
- random: To generate random sleep durations
- requests: For making HTTP requests
- pandas: For organizing the scraped data
- bs4 (BeautifulSoup): For parsing the HTML page
- logging: (Optional) For tracking events, warnings, and errors
"""

import time
import random
import requests
import pandas as pd
from bs4 import BeautifulSoup
# import logging  #(Optional) Use logging to track the scraping process

# Configure logging (currently commented out)
# logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
# Explanation:
# - level=logging.INFO: Show INFO, WARNING, ERROR messages
# - format="%(asctime)s - %(levelname)s - %(message)s": Show time, level, and message nicely formatted


def scrape_sb_nation_articles() -> pd.DataFrame:
    """
    Scrapes the latest articles from the SB Nation homepage.

    Returns:
        pd.DataFrame: A DataFrame containing article titles, authors, publication dates, and article links.
    """
    url = "https://www.sbnation.com"  # Website to scrape
    articles = []  # List to hold the article details

    try:
        # Send HTTP GET request
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an error for bad responses (like 404 or 500)
    except requests.RequestException as e:
        # logging.error(f"Error fetching the page: {e}")  # Log the error if something goes wrong
        return pd.DataFrame()

    # Parse the HTML page using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")
    river = soup.find("div", class_="c-compact-river")  # Container holding all articles

    if not river:
        # logging.warning("Article container not found on the page.")  # Warn if structure is missing
        return pd.DataFrame()

    entries = river.find_all("div", class_="c-compact-river__entry")  # Find all article entries
    # logging.info(f"Found {len(entries)} articles.")  # Log how many articles were found

    for entry in entries:
        body = entry.find("div", class_="c-entry-box--compact__body")
        if not body:
            continue  # Skip if body is missing

        title_tag = body.find("h2", class_="c-entry-box--compact__title")
        title = title_tag.get_text(strip=True) if title_tag else "No Title"
        link = title_tag.find("a")["href"] if title_tag and title_tag.find("a") else "No Link"

        byline = body.find("div", class_="c-byline")
        author_tags = byline.find_all("span", class_="c-byline__author-name") if byline else []
        authors = ", ".join(tag.get_text(strip=True) for tag in author_tags) if author_tags else "Unknown Author"

        time_tag = byline.find("time") if byline else None
        date_published = time_tag.get_text(strip=True) if time_tag else "Unknown Date"

        # Save the scraped article info into the list
        articles.append({
            'Title': title,
            'Author(s)': authors,
            'Date Published': date_published,
            'Article Link': link
        })

        # Sleep for a random time between 1 and 3 seconds to avoid overloading the server
        time.sleep(random.uniform(1, 3))

    # logging.info(f"Scraped {len(articles)} articles successfully.")  # Log the success
    return pd.DataFrame(articles)


# The block below is currently commented out.
# It would normally run the scraper when the script is executed directly.
# Useful when testing this script on its own, but not needed if importing as a module.
"""if __name__ == "__main__":
    
    # Call the scraping function to get the articles
    articles_df = scrape_sb_nation_articles()

    # Check if any articles were scraped
    if not articles_df.empty:
        # logging.info("Sample of scraped data:")  # (Optional) Log that articles were successfully scraped
        print(articles_df.head())  # Display the first few scraped articles
    else:
        # logging.info("No articles were scraped.")  # (Optional) Log that no articles were found
        print("No articles were scraped.")  # Notify user if no data was retrieved

"""