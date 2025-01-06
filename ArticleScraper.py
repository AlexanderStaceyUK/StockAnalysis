import requests
import time
from Article import Article
from datetime import date, timedelta

TODAY = date.today()
TIMEFRAME = timedelta(days=7)  # one week timeframe
START_DATE = TODAY - TIMEFRAME
MAX_CALLS = 7

class ArticleScraper:
    """
    A class that scrapes articles from a specified source within a defined timeframe using the NewsAPI.
    The articles are related to a given keyword, which usually is a company name.
    """

    def __init__(self):
        """
        Initializes the ArticleScraper class.
        """
        pass

    def get_all_articles(self, key):
        """
        Fetches all articles related to a given keyword within the specified timeframe.

        Parameters:
        key (str): The keyword to search for in the articles, usually a company name.

        Returns:
        list[Article]: A list of Article objects containing the fetched articles.
                       Returns -9999 in case of an error.
        """
        try:
            raw_data = self.get_raw_articles(key).json()
            articles_list = self.convert_to_list(raw_data)
            return articles_list
        except Exception as e:
            print(f"An error occurred: {e}")
            return -9999

    def get_raw_articles(self, key):
        """
        Makes an API call to NewsAPI to fetch raw article data related to the given keyword.

        Parameters:
        key (str): The keyword to search for in the articles.

        Returns:
        Response: The raw response object from the NewsAPI containing article data.
        """
        payload = {'q': key, 'apiKey': 'Your_NewsAPI_Key_Here',
                   'from': START_DATE.isoformat(), 'to': TODAY.isoformat(),
                   'sortBy': 'popularity'}
        calls = 0
        api_call = "https://newsapi.org/v2/everything"
        result = requests.get(api_call, params=payload)

        while (calls <= MAX_CALLS and result.status_code != 200):
            time.sleep(10)
            if calls == MAX_CALLS:
                raise Exception("request timed out")
            result = requests.get(api_call, params=payload)

            calls += 1

        return result

    def convert_to_list(self, json_articles):
        """
        Converts the raw JSON article data into a list of Article objects.

        Parameters:
        json_articles (dict): The raw JSON data containing articles.

        Returns:
        list[Article]: A list of Article objects constructed from the raw JSON data.
        """
        if json_articles['status'] != 'ok':
            print("An error occurred")
            print(f"Error code: {json_articles['code']}")
            print(f"Error message: {json_articles['message']}")
            return [] # On an error response, return an empty list

        article_list = [Article(a['title'],
                                a['source']['name'],
                                a['url'],
                                a['publishedAt']) for a in json_articles['articles']]
        return article_list
