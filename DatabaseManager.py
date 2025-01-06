from db_schema import Users, IndustryPreferences, Industry, StockPreferences, Stocks, Companies, Followed, Suggested, News, Notifications
from statistics import mean
from StockScraper import StockScraper
from ArticleAnalysis import ArticleAnalysis
import time
import time
class DatabaseManager:
    """A class to manage database operations for a stock market application."""

    def __init__(self, db):
        """Initialize the DatabaseManager with a database connection, a stock scraper, and an article analysis tool."""
        self.db = db
        self.stock_scraper = StockScraper()
        self.article_analysis = ArticleAnalysis()

    # User methods
    def get_user(self, username):
        """Retrieve a user by their username."""
        try:
            return Users.query.filter_by(Username=username).first()
        except Exception as e:
            print(f"An error occurred while retrieving user: {e}")
            return None

    def get_user_by_id(self, user_id):
        """Retrieve a user by their ID."""
        try:
            return Users.query.get(int(user_id))
        except Exception as e:
            print(f"An error occurred while retrieving user by ID: {e}")
            return None

    def add_user(self, first_name, last_name, username, password, image_data):
        """Add a new user to the database."""
        try:
            new_user = Users(FirstName=first_name, LastName=last_name, Username=username, Password=password, ProfilePic=image_data)
            self.db.session.add(new_user)
            self.db.session.commit()
        except Exception as e:
            print(f"An error occurred while adding a new user: {e}")
            self.db.session.rollback()

    # Companies methods
    def update_all_stocks(self):
        """Update stock information for all companies."""
        try:
            companies = self.get_all_companies()
            for company in companies:
                ticker = company.StockName
                company.CurrentPrice = self.stock_scraper.getCurrentPrice(ticker)
                company.PercentChange = self.stock_scraper.getPercentageChange(ticker)
                company.Volume = self.stock_scraper.getLatestVolume(ticker)
                company.Change = self.stock_scraper.getChange(ticker)
                company.TodaysMax = self.stock_scraper.getMax(ticker)
            self.db.session.commit()
            return 1
        except Exception as e:
            print(f"An error occurred while updating all stocks: {e}")
            self.db.session.rollback()
            return 0

    def update_current_opinion(self, company_id):
        """Update the current opinion metric for a given company based on related news articles."""
        try:
            news = News.query.filter_by(CompanyID=company_id).all()
            if not news:
                print("No news articles found for this company.")
                return 0

            outlook_metrics = [article.OutlookMetric for article in news]
            current_op = round(mean(outlook_metrics))

            opinion_mapping = {-2: "Very Negative", -1: "Slightly Negative", 0: "Average", 1: "Slightly Positive", 2: "Very Positive"}
            current_op_word = opinion_mapping.get(current_op, "Average")

            company = Companies.query.filter_by(CompanyID=company_id).first()
            if not company:
                print("Company not found.")
                return 0

            company.CurrentOpinion = current_op
            company.CurrentOpinionWord = current_op_word
            self.db.session.commit()
            return 1
        except Exception as e:
            print(f"An error occurred while updating current opinion: {e}")
            self.db.session.rollback()
            return 0


    def get_company_by_ticker(self, ticker):
        """Retrieve a company by its stock ticker symbol."""
        try:
            return Companies.query.filter_by(StockName=ticker).first()
        except Exception as e:
            print(f"An error occurred while retrieving company by ticker: {e}")
            return None

    def get_ticker_by_id(self, company_id):
        """Retrieve a company's ticker symbol by its ID."""
        try:
            company = Companies.query.filter_by(CompanyID=company_id).first()
            return company.StockName if company else None
        except Exception as e:
            print(f"An error occurred while retrieving ticker by ID: {e}")
            return None

    def follow_company(self, user_id, company_id):
        """Allow a user to follow a company."""
        try:
            follow = Followed(company_id, user_id)
            self.db.session.add(follow)
            self.db.session.commit()

            news = News.query.filter_by(CompanyID=company_id).limit(5).all()
            for article in news:
                notify = Notifications(article.NewsID, user_id, article.CompanyID, 0, article.Timestamp)
                self.db.session.add(notify)
            self.db.session.commit()
        except Exception as e:
            print(f"An error occurred while following a company: {e}")
            self.db.session.rollback()

    def unfollow_company(self, user_id, company_id):
        """Allow a user to unfollow a company."""
        try:
            Followed.query.filter_by(CompanyID=company_id, UserID=user_id).delete()
            Notifications.query.filter_by(CompanyID=company_id, UserID=user_id).delete()
            self.db.session.commit()
        except Exception as e:
            print(f"An error occurred while unfollowing a company: {e}")
            self.db.session.rollback()

    def get_followed(self, user_id, limit=None):
        """Retrieve companies followed by a user."""
        try:
            if limit is None:
                return Followed.query.filter_by(UserID=user_id).all()
            return Followed.query.filter_by(UserID=user_id).limit(limit).all()
        except Exception as e:
            print(f"An error occurred while retrieving followed companies: {e}")
            return []

    def get_company(self, company_id):
        """Retrieve a company by its ID."""
        try:
            return Companies.query.filter_by(CompanyID=company_id).first()
        except Exception as e:
            print(f"An error occurred while retrieving a company: {e}")
            return None

    def get_all_companies(self):
        """Retrieve all companies in the database."""
        try:
            return Companies.query.all()
        except Exception as e:
            print(f"An error occurred while retrieving all companies: {e}")
            return []

    def get_topcompscroll(self):
        """Retrieve top companies for scrolling based on percent change."""
        try:
            return Companies.query.order_by(Companies.PercentChange.desc()).limit(5).all()
        except Exception as e:
            print(f"An error occurred while retrieving top companies for scrolling: {e}")
            return []

    def get_all_posichange(self):
        """Retrieve all companies with a positive change in stock price."""
        try:
            return Companies.query.filter_by(Change=1).all()
        except Exception as e:
            print(f"An error occurred while retrieving companies with positive change: {e}")
            return []

    def get_all_posiop(self):
        """Retrieve all companies with a positive opinion metric."""
        try:
            return Companies.query.filter(Companies.CurrentOpinion > 0).all()
        except Exception as e:
            print(f"An error occurred while retrieving companies with positive opinion: {e}")
            return []

    def get_top_perc_change(self, limit):
        """Retrieve top companies based on percentage change."""
        try:
            return Companies.query.order_by(Companies.PercentChange.desc()).limit(limit).all()
        except Exception as e:
            print(f"An error occurred while retrieving top companies by percentage change: {e}")
            return []

    def get_top_yield_comp(self, limit):
        """Retrieve top companies based on yield."""
        try:
            return Companies.query.order_by(Companies.Yield.desc()).limit(limit).all()
        except Exception as e:
            print(f"An error occurred while retrieving top companies by yield: {e}")
            return []

    def get_top_priced_comp_inds(self, industry, limit):
        """Retrieve top priced companies within a specific industry."""
        try:
            return Companies.query.filter_by(IndustryName=industry).order_by(Companies.CurrentPrice.desc()).limit(limit).all()
        except Exception as e:
            print(f"An error occurred while retrieving top priced companies in industry: {e}")
            return []

    def get_top_priced_comp_stock(self, stock_type, limit):
        """Retrieve top priced companies of a specific stock type."""
        try:
            return Companies.query.filter_by(StockType=stock_type).order_by(Companies.CurrentPrice.desc()).limit(limit).all()
        except Exception as e:
            print(f"An error occurred while retrieving top priced companies by stock type: {e}")
            return []

    def get_all_comp_inds(self, industry):
        """Retrieve all companies within a specific industry."""
        try:
            return Companies.query.filter_by(IndustryName=industry).all()
        except Exception as e:
            print(f"An error occurred while retrieving all companies in industry: {e}")
            return []

    def get_all_comp_stock(self, stock_type):
        """Retrieve all companies of a specific stock type."""
        try:
            return Companies.query.filter_by(StockType=stock_type).all()
        except Exception as e:
            print(f"An error occurred while retrieving all companies by stock type: {e}")
            return []

    def get_all_comp_in_search(self, search_parameter):
        """Search for companies by name or ticker."""
        try:
            return Companies.query.filter(Companies.Name.like(search_parameter) | Companies.StockName.like(search_parameter)).all()
        except Exception as e:
            print(f"An error occurred while searching for companies: {e}")
            return []

    def is_name_in_search(self, company_id, search_parameter):
        """Check if a company name or ticker matches a search parameter."""
        try:
            return Companies.query.filter((Companies.CompanyID == company_id) & (Companies.Name.like(search_parameter) | Companies.StockName.like(search_parameter))).first() is not None
        except Exception as e:
            print(f"An error occurred while checking if name is in search: {e}")
            return False

    def is_comp_in_industry(self, company_id, industry_name):
        """Check if a company belongs to a specific industry."""
        try:
            return Companies.query.filter((Companies.CompanyID == company_id) & (Companies.IndustryName == industry_name)).first() is not None
        except Exception as e:
            print(f"An error occurred while checking if company is in industry: {e}")
            return False

    def is_comp_in_stock(self, company_id, stock_type):
        """Check if a company belongs to a specific stock type."""
        try:
            return Companies.query.filter((Companies.CompanyID == company_id) & (Companies.StockType == stock_type)).first() is not None
        except Exception as e:
            print(f"An error occurred while checking if company is in stock type: {e}")
            return False

    def is_comp_posichnge(self, company_id):
        """Check if a company has a positive change in stock price."""
        try:
            return Companies.query.filter((Companies.CompanyID == company_id) & (Companies.Change == 1)).first() is not None
        except Exception as e:
            print(f"An error occurred while checking if company has positive change: {e}")
            return False



    def is_comp_posiop(self, company_id):
        """Check if a company has a positive opinion."""
        try:
            return Companies.query.filter((Companies.CompanyID == company_id) & (Companies.CurrentOpinion >= 1)).first() is not None
        except Exception as e:
            print(f"An error occurred while checking for positive opinion: {e}")
            return False

    # Followers
    def is_followed(self, user_id, company_id):
        """Check if a user is following a company."""
        try:
            return Followed.query.filter_by(CompanyID=company_id, UserID=user_id).first() is not None
        except Exception as e:
            print(f"An error occurred while checking if a company is followed: {e}")
            return False

    # Industries
    def get_all_industries(self):
        """Retrieve all industries from the database."""
        try:
            return Industry.query.all()
        except Exception as e:
            print(f"An error occurred while retrieving all industries: {e}")
            return []

    # Stocks
    def get_all_stock_types(self):
        """Retrieve all stock types from the database."""
        try:
            return Stocks.query.all()
        except Exception as e:
            print(f"An error occurred while retrieving all stock types: {e}")
            return []

    # Notifications
    def update_notifications(self):
        """Update notifications - Method implementation depends on specific requirements."""
        pass  # Implement as needed, including error handling

    def mark_all_read(self, uname):
        """Mark all notifications for a user as read."""
        try:
            user_id = Users.query.filter_by(Username=uname).first().id
            notifications = Notifications.query.filter_by(UserID=user_id).all()
            for notify in notifications:
                notify.Read = 1
            self.db.session.commit()
        except Exception as e:
            print(f"An error occurred while marking notifications as read: {e}")
            self.db.session.rollback()

    def read_notification(self, news_id, uname):
        """Mark a specific notification as read."""
        try:
            user_id = Users.query.filter_by(Username=uname).first().id
            notification = Notifications.query.filter_by(NewsID=news_id, UserID=user_id).first()
            if notification:
                notification.Read = 1
                self.db.session.commit()
        except Exception as e:
            print(f"An error occurred while reading a notification: {e}")
            self.db.session.rollback()

    def get_user_notification(self, user_id, limit=None):
        """Retrieve unread notifications for a user."""
        try:
            if limit is None:
                return Notifications.query.filter_by(UserID=user_id, Read=0).all()
            return Notifications.query.filter_by(UserID=user_id, Read=0).limit(limit).all()
        except Exception as e:
            print(f"An error occurred while retrieving user notifications: {e}")
            return []

    def get_all_ord_notifications(self, user_id):
        """Retrieve all notifications for a user, ordered by read status and timestamp."""
        try:
            return Notifications.query.filter_by(UserID=user_id).order_by(Notifications.Read).order_by(Notifications.Timestamp.desc()).all()
        except Exception as e:
            print(f"An error occurred while retrieving ordered notifications: {e}")
            return []

    def get_top_notifications(self, user_id, limit):
        """Retrieve top notifications for a user based on read status and timestamp."""
        try:
            return Notifications.query.filter_by(UserID=user_id).order_by(Notifications.Read.asc()).order_by(Notifications.Timestamp.desc()).limit(limit).all()
        except Exception as e:
            print(f"An error occurred while retrieving top notifications: {e}")
            return []

    # News
    def update_all_news(self):
        """Update news for all companies."""
        try:
            companies = self.get_all_companies()
            for company in companies:
                articles = self.article_analysis.analyseAllArticles(company.Name)
                self.update_news(ticker=company.StockName, articles=articles)
            return 1
        except Exception as e:
            print(f"An error occurred while updating all news: {e}")
            self.db.session.rollback()
            return 0

    def update_news(self, ticker, articles):
        """Update news for a specific company."""
        try:
            comp_id = self.get_company_by_ticker(ticker)
            if comp_id is None:
                print(f"No company found for ticker {ticker}")
                return 0

            for article in articles:
                new_article = News(Headline=article.headline, Photo=article.photo, SourceName=article.source_name, SourceURL=article.url, OutlookMetric=article.sentiment_value, CompanyID=comp_id, Timestamp=article.timestamp)
                self.db.session.add(new_article)
                if article.sentiment_value < 0.3 or article.sentiment_value > 0.7:
                    followers = Followed.query.filter_by(CompanyID=comp_id).all()
                    for user in followers:
                        notify = Notifications(UserID=user.UserID, NewsID=new_article.NewsID, CompanyID=comp_id, Read=0, Timestamp=article.timestamp)
                        self.db.session.add(notify)
            self.db.session.commit()
            return 1
        except Exception as e:
            print(f"An error occurred while updating news for ticker {ticker}: {e}")
            self.db.session.rollback()
            return 0

    def get_news(self, news_id):
        """Retrieve a specific news item by its ID."""
        try:
            return News.query.filter_by(NewsID=news_id).first()
        except Exception as e:
            print(f"An error occurred while retrieving news item: {e}")
            return None

    def get_all_latest_news(self):
        """Retrieve all news items, ordered by timestamp descending."""
        try:
            return News.query.order_by(News.Timestamp.desc()).all()
        except Exception as e:
            print(f"An error occurred while retrieving all latest news: {e}")
            return []

    def get_news_desc(self, limit):
        """Retrieve a limited number of news items, ordered by ID descending."""
        try:
            return News.query.order_by(News.NewsID.desc()).limit(limit).all()
        except Exception as e:
            print(f"An error occurred while retrieving news items with limit: {e}")
            return []

    def get_comp_news_desc(self, company_id, limit):
        """Retrieve news for a specific company, limited and ordered by ID descending."""
        try:
            return News.query.filter_by(CompanyID=company_id).order_by(News.NewsID.desc()).limit(limit).all()
        except Exception as e:
            print(f"An error occurred while retrieving company-specific news with limit: {e}")
            return []

    def get_company_news(self, company_id):
        """Retrieve all news items for a specific company, ordered by timestamp descending."""
        try:
            return News.query.filter_by(CompanyID=company_id).order_by(News.Timestamp.desc()).all()
        except Exception as e:
            print(f"An error occurred while retrieving company-specific news: {e}")
            return []

    # Stock preferences
    def get_all_user_stock(self, user_id):
        """Retrieve all stock preferences for a user."""
        try:
            return StockPreferences.query.filter_by(User_ID=user_id).all()
        except Exception as e:
            print(f"An error occurred while retrieving user stock preferences: {e}")
            return []

    def add_stock_pref(self, user_id, stock_type):
        """Add a stock preference for a user."""
        try:
            new_pref = StockPreferences(User_ID=user_id, StockType=stock_type)
            self.db.session.add(new_pref)
            self.db.session.commit()
        except Exception as e:
            print(f"An error occurred while adding stock preference: {e}")
            self.db.session.rollback()

    def delete_all_stock_pref(self, user_id):
        """Delete all stock preferences for a user."""
        try:
            StockPreferences.query.filter_by(User_ID=user_id).delete()
            self.db.session.commit()
        except Exception as e:
            print(f"An error occurred while deleting all stock preferences: {e}")
            self.db.session.rollback()

    def delete_stock_pref(self, user_id, stock_type):
        """Delete a specific stock preference for a user."""
        try:
            pref = StockPreferences.query.filter_by(User_ID=user_id, StockType=stock_type).first()
            if pref:
                self.db.session.delete(pref)
                self.db.session.commit()
        except Exception as e:
            print(f"An error occurred while deleting stock preference: {e}")
            self.db.session.rollback()

    # Industry preferences
    def get_all_user_ind(self, user_id):
        """Retrieve all industry preferences for a user."""
        try:
            return IndustryPreferences.query.filter_by(User_ID=user_id).all()
        except Exception as e:
            print(f"An error occurred while retrieving user industry preferences: {e}")
            return []

    def delete_all_industry_pref(self, user_id):
        """Delete all industry preferences for a user."""
        try:
            IndustryPreferences.query.filter_by(User_ID=user_id).delete()
            self.db.session.commit()
        except Exception as e:
            print(f"An error occurred while deleting all industry preferences: {e}")
            self.db.session.rollback()

    def add_industry_pref(self, user_id, industry_type):
        """Add an industry preference for a user."""
        try:
            new_pref = IndustryPreferences(User_ID=user_id, IndustryName=industry_type)
            self.db.session.add(new_pref)
            self.db.session.commit()
        except Exception as e:
            print(f"An error occurred while adding industry preference: {e}")
            self.db.session.rollback()

    def delete_industry_pref(self, user_id, industry_type):
        """Delete a specific industry preference for a user."""
        try:
            pref = IndustryPreferences.query.filter_by(User_ID=user_id, IndustryName=industry_type).first()
            if pref:
                self.db.session.delete(pref)
                self.db.session.commit()
        except Exception as e:
            print(f"An error occurred while deleting industry preference: {e}")
            self.db.session.rollback()

    # Suggested companies
    def get_all_suggested(self, user_id, limit):
        """Retrieve a limited number of suggested companies for a user."""
        try:
            return Suggested.query.filter_by(UserID=user_id).limit(limit).all()
        except Exception as e:
            print(f"An error occurred while retrieving suggested companies: {e}")
            return []

    def get_all_ord_suggested(self, user_id):
        """Retrieve suggested companies for a user, ordered by suggest metric descending."""
        try:
            return Suggested.query.filter_by(UserID=user_id).order_by(Suggested.SuggestMetric.desc()).all()
        except Exception as e:
            print(f"An error occurred while retrieving ordered suggested companies: {e}")
            return []

    def initialize_all_companies(self):
        """A method that allows to intialize any of the company below by uncommenting, due to api requests limits these restricted"""
        pass
        # self.add_company(name="3i", ticker="III", industry="Financial Services")
        # self.add_company(name="Admiral Group", ticker="ADM", industry="Insurance")
        # self.add_company(name="Airtel Africa", ticker="AAF", industry="Telecommunications Services")
        # self.add_company(name="Anglo American plc", ticker="AAL", industry="Mining")
        # self.add_company(name="Antofagasta plc", ticker="ANTO", industry="Mining")
        # self.add_company(name="Ashtead Group", ticker="AHT", industry="Support Services")
        # self.add_company(name="Associated British Foods", ticker="ABF", industry="Food & Tobacco")
        # self.add_company(name="AstraZeneca", ticker="AZN", industry="Pharmaceuticals & Biotechnology")
        # self.add_company(name="Auto Trader Group", ticker="AUTO", industry="Media")
        # self.add_company(name="Aviva", ticker="AV", industry="Life Insurance")
        # self.add_company(name="B&M", ticker="BME", industry="Retailers")
        # self.add_company(name="BAE Systems", ticker="BA", industry="Aerospace & Defence")
        # self.add_company(name="Barclays", ticker="BARC", industry="Banks")
        # self.add_company(name="Barratt Developments", ticker="BDEV", industry="Household Goods & Home Construction")
        # self.add_company(name="Beazley Group", ticker="BEZ", industry="Insurance")
        # self.add_company(name="Berkeley Group Holdings", ticker="BKG", industry="Household Goods & Home Construction")
        # self.add_company(name="BP", ticker="BP", industry="Oil & Gas Producers")
        # self.add_company(name="British American Tobacco", ticker="BATS", industry="Tobacco")
        # self.add_company(name="BT Group", ticker="BT", industry="Telecommunications Services")
        # self.add_company(name="Bunzl", ticker="BNZL", industry="Support Services")
        # self.add_company(name="Burberry", ticker="BRBY", industry="Personal Goods")
        # self.add_company(name="Centrica", ticker="CNA", industry="Multiline Utilities")
        # self.add_company(name="Coca-Cola Hellenic Bottling Company|Coca-Cola HBC", ticker="CCH", industry="Beverages")
        # self.add_company(name="Compass Group", ticker="CPG", industry="Support Services")
        # self.add_company(name="Convatec", ticker="CTEC", industry="Health Care Equipment & Supplies")
        # self.add_company(name="Croda International", ticker="CRDA", industry="Chemicals")
        # self.add_company(name="DCC plc", ticker="DCC", industry="Support Services")
        # self.add_company(name="Diageo", ticker="DGE", industry="Beverages")
        # self.add_company(name="Diploma plc|Diploma", ticker="DPLM", industry="Industrial Support Services")
        # self.add_company(name="Endeavour Mining", ticker="EDV", industry="Mining")
        # self.add_company(name="Entain", ticker="ENT", industry="Travel & Leisure")
        # self.add_company(name="Experian", ticker="EXPN", industry="Support Services")
        # self.add_company(name="Foreign & Colonial Investment Trust", ticker="FCIT", industry="Financial Services")
        # self.add_company(name="Flutter Entertainment", ticker="FLTR", industry="Travel & Leisure")
        # self.add_company(name="Frasers Group", ticker="FRAS", industry="Retailers")
        # self.add_company(name="Fresnillo plc", ticker="FRES", industry="Mining")
        # self.add_company(name="Glencore", ticker="GLEN", industry="Mining")
        # self.add_company(name="GSK plc", ticker="GSK", industry="Pharmaceuticals & Biotechnology")
        # self.add_company(name="Haleon", ticker="HLN", industry="Pharmaceuticals & Biotechnology")
        # self.add_company(name="Halma plc", ticker="HLMA", industry="Electronic Equipment & Parts")
        # self.add_company(name="Hikma Pharmaceuticals", ticker="HIK", industry="Pharmaceuticals & Biotechnology")
        # self.add_company(name="Howdens Joinery", ticker="HWDN", industry="Homebuilding & Construction Supplies")
        # self.add_company(name="HSBC", ticker="HSBA", industry="Banks")
        # self.add_company(name="IHG Hotels & Resorts", ticker="IHG", industry="Travel & Leisure")
        # self.add_company(name="IMI plc|IMI", ticker="IMI", industry="Machinery, Tools, Heavy Vehicles, Trains & Ships")
        # self.add_company(name="Imperial Brands", ticker="IMB", industry="Tobacco")
        # self.add_company(name="Informa", ticker="INF", industry="Media")
        # self.add_company(name="Intermediate Capital Group", ticker="ICP", industry="Financial Services")
        # self.add_company(name="International Airlines Group", ticker="IAG", industry="Travel & Leisure")
        # self.add_company(name="Intertek", ticker="ITRK", industry="Support Services")
        # self.add_company(name="JD Sports", ticker="JD", industry="General Retailers")
        # self.add_company(name="Kingfisher plc", ticker="KGF", industry="Retailers")
        # self.add_company(name="Landsec|Land Securities", ticker="LAND", industry="Real Estate Investment Trusts")
        # self.add_company(name="Legal & General", ticker="LGEN", industry="Life Insurance")
        # self.add_company(name="Lloyds Banking Group", ticker="LLOY", industry="Banks")
        # self.add_company(name="London Stock Exchange Group", ticker="LSEG", industry="Financial Services")
        # self.add_company(name="M&G", ticker="MNG", industry="Financial Services")
        # self.add_company(name="Marks & Spencer", ticker="MKS", industry="Food & Drug Retailing")
        # self.add_company(name="Melrose Industries", ticker="MRO", industry="Aerospace & Defence")
        # self.add_company(name="Mondi", ticker="MNDI", industry="Containers & Packaging")
        # self.add_company(name="National Grid plc", ticker="NG", industry="Multiline Utilities")
        # self.add_company(name="NatWest Group", ticker="NWG", industry="Banks")
        # self.add_company(name="Next plc", ticker="NXT", industry="General Retailers")
        # self.add_company(name="Ocado|Ocado Group", ticker="OCDO", industry="Food & Drug Retailers")
        # self.add_company(name="Pearson plc", ticker="PSON", industry="Media")
        # self.add_company(name="Pershing Square Holdings", ticker="PSH", industry="Financial Services")
        # self.add_company(name="Persimmon plc|Persimmon", ticker="PSN", industry="Household Goods & Home Construction")
        # self.add_company(name="Phoenix Group", ticker="PHNX", industry="Life Insurance")
        # self.add_company(name="Prudential plc", ticker="PRU", industry="Life Insurance")
        # self.add_company(name="Reckitt", ticker="RKT", industry="Household Goods & Home Construction")
        # self.add_company(name="RELX", ticker="REL", industry="Media")
        # self.add_company(name="Rentokil Initial", ticker="RTO", industry="Support Services")
        # self.add_company(name="Rightmove", ticker="RMV", industry="Media")
        # self.add_company(name="Rio Tinto (corporation)|Rio Tinto", ticker="RIO", industry="Mining")
        # self.add_company(name="Rolls-Royce Holdings", ticker="RR", industry="Aerospace & Defence")
        # self.add_company(name="RS Group plc", ticker="RS1", industry="Industrials")
        # self.add_company(name="Sage Group", ticker="SGE", industry="Software & Computer Services")
        # self.add_company(name="Sainsbury's", ticker="SBRY", industry="Food & Drug Retailing")
        # self.add_company(name="Schroders", ticker="SDR", industry="Financial Services")
        # self.add_company(name="Scottish Mortgage Investment Trust", ticker="SMT", industry="Collective Investments")
        # self.add_company(name="Segro", ticker="SGRO", industry="Real Estate Investment Trusts")
        # self.add_company(name="Severn Trent", ticker="SVT", industry="Multiline Utilities")
        # self.add_company(name="Shell plc", ticker="SHEL", industry="Oil & Gas Producers")
        # self.add_company(name="DS Smith", ticker="SMDS", industry="General Industrials")
        # self.add_company(name="Smiths Group", ticker="SMIN", industry="General Industrials")
        # self.add_company(name="Smith & Nephew", ticker="SN", industry="Health Care Equipment & Supplies")
        # self.add_company(name="Smurfit Kappa", ticker="SKG", industry="General Industrials")
        # self.add_company(name="Spirax-Sarco Engineering", ticker="SPX", industry="Industrial Engineering")
        # self.add_company(name="SSE plc", ticker="SSE", industry="Electrical Utilities & Independent Power Producers")
        # self.add_company(name="Standard Chartered", ticker="STAN", industry="Banks")
        # self.add_company(name="St. James's Place plc", ticker="STJ", industry="Financial Services")
        # self.add_company(name="Taylor Wimpey", ticker="TW", industry="Household Goods & Home Construction")
        self.add_company(name="Tesco", ticker="TSCO", industry="Food & Drug Retailing")
        self.add_company(name="Unilever", ticker="ULVR", industry="Personal Goods")
        # self.add_company(name="United Utilities", ticker="UU", industry="Multiline Utilities")
        # self.add_company(name="Unite Students|Unite Group", ticker="UTG", industry="Real Estate Investment Trusts")
        # self.add_company(name="Vodafone|Vodafone Group", ticker="VOD", industry="Mobile Telecommunications")
        # self.add_company(name="Weir Group", ticker="WEIR", industry="Industrial Goods and Services")
        # self.add_company(name="Whitbread", ticker="WTB", industry="Retail hospitality")
        # self.add_company(name="WPP plc", ticker="WPP", industry="Media")

    def add_company(self, name, ticker, industry):
        """Add a new company to the database."""
        try:
            with open('src/static/images/sample_logo.webp', 'rb') as file:
                image_data = file.read()

            new_company = Companies(
                Name=name,
                Logo=image_data,
                StockName=ticker,
                CurrentPrice=0,
                LastChange=0,
                PercentChange=0,
                Change=0,
                Volume=0,
                TodaysMax=0,
                TodaysMin=0,
                PreviousClose=0,
                IndustryName=industry,
                StockType="N/A",
                Yield=0,
                CurrentOpinion=0,
                CurrentOpinionWord=0,
                Parent="N/A",
                Founder="N/A",
                CEO="N/A",
                OneYearTarget=0,
                MaxInTotal=0,
                PredictedPriceChange=0,
                PriceChangeDirection=0,
                Graph_1d=None,
                Graph_5d=None,
                Graph_1m=None,
                Graph_6m=None,
                Graph_1y=None,
                PriceDay1=0,
                PriceDay2=0,
                PriceDay3=0,
                PriceDay4=0,
                PriceDay5=0,
                PriceDay6=0,
                PriceDay7=0,
                PriceDay8=0,
                PriceDay9=0,
                PriceDay10=0,
                PriceDay11=0,
                PriceDay12=0,
                PriceDay13=0,
                PriceDay14=0,
                PriceDay15=0,
                PriceDay16=0,
                PriceDay17=0,
                PriceDay18=0,
                PriceDay19=0,
                PriceDay20=0,
                PriceDay21=0,
                PriceDay22=0,
                PriceDay23=0,
                PriceDay24=0,
                PriceDay25=0,
                PriceDay26=0,
                PriceDay27=0,
                PriceDay28=0,
                PriceDay29=0,
                PriceDay30=0,
                PriceHour9=0,
                PriceHour10=0,
                PriceHour11=0,
                PriceHour12=0,
                PriceHour13=0,
                PriceHour14=0,
                PriceHour15=0,
            )
            self.db.session.add(new_company)
            self.db.session.commit()
        except Exception as e:
            print(f"An error occurred while adding a company: {e}")
            self.db.session.rollback()
