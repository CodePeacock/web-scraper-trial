"""This script takes a list of URLs as input and returns the HTML content of the webpage."""
import concurrent.futures

import pandas as pd
import requests
from bs4 import BeautifulSoup

# set connection and timeout settings for requests
REQUESTS_TIMEOUT = 10
# REQUESTS_RETRY_COUNT = 3


def url_ok(url):
    """This function checks if the URL is valid or not."""
    try:
        request = requests.head(url, timeout=REQUESTS_TIMEOUT)
        return request.status_code == 200
    except requests.exceptions.RequestException:
        return False


def scrape_url(url):
    """This function takes a URL as input and returns the HTML content of the webpage."""
    if not url_ok(url):
        return None

    try:
        return get_data(url)
    except requests.exceptions.RequestException:
        return None


def get_data(url):
    """This function takes a URL as input and returns the HTML content of the webpage."""
    page = requests.get(url, timeout=REQUESTS_TIMEOUT)
    page.raise_for_status()  # raise an exception for non-200 response status codes
    soup = BeautifulSoup(page.content, "html.parser")

    articlecontent = soup.find("div", class_="td-post-content").text
    articletitle = soup.find("h1", class_="entry-title").text
    return articlecontent, articletitle


def scrape_urls(urls):
    """This function scrapes a list of URLs and returns a list of scraped data."""
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(scrape_url, urls)
        scraped_data = [data for data in results if data is not None]
    return scraped_data


def write_data_to_file(url_id, articlecontent, articletitle):
    """This function writes the article content and title to a text file."""
    with open(f"scrapedfiles/{url_id}.txt", "w+", encoding="utf-8") as file:
        file.write(f"Article Title: {articletitle}\n")
        file.write(f"Article Content: {articlecontent}\n")


def iterate():
    """This function iterates through the list of URLs and calls the scraper function."""
    dataframe = pd.read_excel("Input.xlsx", usecols="A,B")
    urls = dataframe["URL"].tolist()
    url_ids = dataframe["URL_ID"].tolist()
    scraped_data = scrape_urls(urls)
    for i, data in enumerate(scraped_data):
        write_data_to_file(url_ids[i], data[0], data[1])


if __name__ == "__main__":
    iterate()


# """This script takes a list of URLs as input and returns the HTML content of the webpage."""
# import logging

# import pandas as pd
# import requests
# from bs4 import BeautifulSoup

# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s [%(levelname)s] %(message)s",
#     handlers=[logging.FileHandler("debug.log"), logging.StreamHandler()],
# )


# def url_ok(url):
#     """This function checks if the URL is valid or not."""
#     r = requests.head(url, timeout=5)
#     return r.status_code == 200


# def scraper(url: str):
#     """This function takes a URL as input and returns the HTML content of the webpage."""
#     if url_ok(url) is False:
#         return None

#     page = requests.get(url, timeout=10).text
#     soup = BeautifulSoup(page, "html.parser")

#     articlecontent = soup.find("div", class_="td-post-content").text
#     articletitle = soup.find("h1", class_="entry-title").text
#     return articlecontent, articletitle


# df = pd.read_excel("Input.xlsx", usecols="A,B")
# # print(df["URL"][1])


# def iterate():
#     """This function iterates through the list of URLs and calls the scraper function."""
#     for i in range(len(df["URL"])):
#         if scraper(df["URL"][i]) is not None:
#             # scraper(df["URL"][i])
#             print(df["URL_ID"][i])
#         else:
#             logging.info("URL not found")
#             continue

#         with open(f"scraped/{df['URL_ID'][i]}.txt", "w+", encoding="utf-8") as file:
#             filewrites(file, i)


# def filewrites(file, i):
#     """This function writes the article content and title to a text file."""
#     file.write("Article Title: ")
#     URL = scraper(df["URL"][i])[1]
#     file.write(f"scraped{URL}")
#     file.write("\n")
#     file.write("Article Content: ")
#     URL = scraper(df["URL"][i])[0]
#     file.write(scraper(df["URL"][i])[0])
#     file.close()


# # except Exception as e:
# #     print(e)


# iterate()
