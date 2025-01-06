from polygon import RESTClient
from json_handler import JsonHandler

from datetime import date, timedelta, datetime
import calendar
class StockScraper:
    def __init__(self):
        try:
            self.client = RESTClient(api_key = "ENAbkJjikS7QsENMzSLdwnPsDozKCdTz")
            self.YESTERDAY = datetime.now() - timedelta(days=1)
            TIMEFRAME = timedelta(days=30) # one month timeframe
            START_DATE = self.YESTERDAY - TIMEFRAME
            self.YESTERDAYFORMATTED = self.YESTERDAY.strftime('%Y-%m-%d')
            self.STARTDATEFORMATTED = START_DATE.strftime('%Y-%m-%d')
            time = self.YESTERDAY - timedelta(days=1)
            self.TIMEFORMATTED = time.strftime('%Y-%m-%d')


            # If today is sunday, subtract a day off
        except Exception as e:
            print(f"An error occurred: {e}")

    #Auxiliary Functions
    def getStockPrices(self, ticker):
        try:
            aggs = []
            for a in self.client.list_aggs(ticker="AAPL", multiplier=1, timespan="day", from_=self.STARTDATEFORMATTED, to=self.YESTERDAYFORMATTED, limit=50000):
                aggs.append(a.vwap)
            return aggs
        except Exception as e:
            print(f"An error occurred: {e}")
            return -9999

    def getLatestVolume(self, ticker):
        try:
            volume = self.client.get_daily_open_close_agg(ticker, self.YESTERDAYFORMATTED).volume
            return volume
        except Exception as e:
            print(f"An error occurred: {e}")
            return -9999
        
    def getMax(self, ticker):
        try:
            max = self.client.get_daily_open_close_agg(ticker, self.YESTERDAYFORMATTED).high
            return max
        except Exception as e:
            print(f"An error occurred: {e}")
            return -9999

    def getMin(self, ticker):
        try:
            min = self.client.get_daily_open_close_agg(ticker, self.YESTERDAYFORMATTED).low
            return min
        except Exception as e:
            print(f"An error occurred: {e}")
            return -9999

    def getCurrentPrice(self,ticker):
        try:
            current = self.client.get_daily_open_close_agg(ticker, self.YESTERDAYFORMATTED).close
            return current
        except Exception as e:
            print(f"An error occurred: {e}")
            return -9999
    def getPercentageChange(self, ticker):
        try:
            initialPrice = self.client.get_daily_open_close_agg(ticker, self.TIMEFORMATTED).close
            finalPrice = self.getCurrentPrice(ticker)
            
            percentageChange = ((finalPrice-initialPrice)/abs(initialPrice))*100
            return percentageChange
        except Exception as e:
            print(f"An error occurred: {e}")
            return -9999

    def getChange(self, ticker):
        try:
            initialPrice = self.client.get_daily_open_close_agg(ticker, self.TIMEFORMATTED).close
            finalPrice = self.getCurrentPrice(ticker)

            change = finalPrice-initialPrice
            return change
        except Exception as e:
            print(f"An error occurred: {e}")
            return -9999

    def getPreviousClose(self,ticker):
        try:
            dayBeforeYesterday = (self.YESTERDAY - timedelta(days=1)).strftime('%Y-%m-%d')

            previousClose = self.client.get_daily_open_close_agg(ticker, dayBeforeYesterday).close
            return previousClose
        except Exception as e:
            print(f"An error occurred: {e}")
            return -9999

