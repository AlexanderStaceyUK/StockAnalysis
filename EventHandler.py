import threading
import time

class EventHandler:
    """
    A class designed to handle periodic updates to stock data and news articles by
    running two separate threads. One thread updates stock data at specified intervals,
    and the other updates news articles at different intervals.
    """

    def __init__(self, DatabaseMan):
        """
        Initializes the EventHandler class with a reference to a database manager and sets up threading for periodic updates.

        Parameters:
        DatabaseMan: An instance of a database management class responsible for updating stock data and news articles in the database.
        """
        self.DatabaseMan = DatabaseMan
        self.stock_interval = 20  # Interval for updating stock data in minutes
        self.article_interval = 24  # Interval for updating news articles in hours

        # Creating threads for stock and article updates
        self.thread1 = threading.Thread(target=self.stock_thread)
        self.thread2 = threading.Thread(target=self.article_thread)

        # Starting the threads
        self.thread1.start()
        self.thread2.start()

    def stock_thread(self):
        """
        A method that runs in a separate thread to periodically update stock data.
        The update interval is defined by `self.stock_interval`.
        """
        while True:
            self.DatabaseMan.update_all_Stocks()  # Calls the method to update all stock data
            time.sleep(self.stock_interval * 60)  # Sleeps for `stock_interval` minutes

    def article_thread(self):
        """
        A method that runs in a separate thread to periodically update news articles.
        The update interval is defined by `self.article_interval`.
        """
        while True:
            self.DatabaseMan.update_all_News()  # Calls the method to update all news articles
            time.sleep(self.article_interval * 3600)  # Sleeps for `article_interval` hours
