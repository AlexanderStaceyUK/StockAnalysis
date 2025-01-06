class Article:
    # Constructor for the Article class
    def __init__(self, headline, s_name, url, timestamp, sentiment_value=0.0):
        # headline: The title of the article
        self.headline = headline
        
        # source_name: The name of the source from which the article was obtained
        self.source_name = s_name
        
        # url: The web address where the article can be found
        self.url = url
        
        # timestamp: The date and time the article was published
        self.timestamp = timestamp
        
        # sentiment_value: A numerical value representing the sentiment analysis of the article
        # Default value is set to 0.0
        self.sentiment_value = sentiment_value
        
        # photo: A placeholder for a potential photo associated with the article
        # Initialized as an empty string, assuming it might be set later
        self.photo = ""

    # String representation of the Article instance
    def __str__(self) -> str:
        # Returns a string that concatenates the article's headline, source name, URL, and timestamp
        return self.headline + ", " + self.source_name + ", " + self.url + ", " + self.timestamp
