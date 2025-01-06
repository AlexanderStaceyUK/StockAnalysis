from textblob import Blobber
from textblob.sentiments import NaiveBayesAnalyzer
from ArticleScraper import ArticleScraper 

class ArticleAnalysis:
    """
    A class responsible for analyzing the sentiment of articles using the NaiveBayesAnalyzer.
    It utilizes an ArticleScraper object to fetch articles for a given company and then
    applies sentiment analysis to each article's headline.
    """

    def __init__(self):
        """
        Initializes the ArticleAnalysis class by setting up the sentiment analysis tool
        with NaiveBayesAnalyzer and creating an ArticleScraper instance.
        """
        self.AnalysisFactory = Blobber(analyzer=NaiveBayesAnalyzer())
        self.scraper = ArticleScraper()

    def analyseArticle(self, article):
        """
        Analyzes the sentiment of a single article's headline.

        Parameters:
        article (Article): An Article object containing information like the headline to be analyzed.

        Returns:
        float: The positivity score of the article's headline sentiment.
        """
        analyser = self.AnalysisFactory(article.headline)
        return analyser.sentiment[1]

    def analyseAllArticles(self, company):
        """
        Fetches all articles for a given company using the ArticleScraper and
        performs sentiment analysis on each article's headline.

        Parameters:
        company (str): The name of the company for which articles are to be analyzed.

        Returns:
        list[Article]: A list of Article objects with updated sentiment values.
                       Returns an empty list in case of an error.
        """
        try:
            articles = []
            for article in self.scraper.get_all_articles(company):
                article.sentiment_value = self.analyseArticle(article)
                articles.append(article)
            return articles
        except Exception as e:
            print(f"An error occurred: {e}")
            return []
