from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Users(UserMixin, db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(100), nullable=False)
    LastName = db.Column(db.String(100), nullable=False)
    Username = db.Column(db.String(100), unique=True, nullable=False)
    Password = db.Column(db.String(100), nullable=False)
    ProfilePic = db.Column(db.BLOB)

    def __init__(self, FirstName, LastName, Username, Password, ProfilePic):
        self.FirstName = FirstName
        self.LastName = LastName
        self.Username = Username
        self.Password = Password
        self.ProfilePic = ProfilePic

class IndustryPreferences(db.Model):
    __tablename__='industry_preferences'
    User_ID = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    IndustryName = db.Column(db.String(100), db.ForeignKey('industries.IndustryName'), primary_key=True)

    def __init__(self, User_ID, IndustryName):
        self.User_ID = User_ID
        self.IndustryName = IndustryName

class Industry(db.Model):
    __tablename__='industries'
    IndustryName = db.Column(db.String(100), primary_key=True)

    def __init__(self, IndustryName):
        self.IndustryName = IndustryName

class StockPreferences(db.Model):
    __tablename__='stock_preferences'
    User_ID = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    StockType = db.Column(db.String(100), db.ForeignKey('stocks.StockType'), primary_key=True)

    def __init__(self, User_ID, StockType):
        self.User_ID = User_ID
        self.StockType = StockType

class Stocks(db.Model):
    __tablename__='stocks'
    StockType = db.Column(db.String(100), primary_key=True)

    def __init__(self, StockType):
        self.StockType = StockType

class Companies(db.Model):
    __tablename__='companies'
    CompanyID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Logo = db.Column(db.BLOB)
    StockName = db.Column(db.String(100), unique=True, nullable=False)
    CurrentPrice = db.Column(db.Numeric(precision=10, scale=2))
    LastChange = db.Column(db.Integer)
    PercentChange = db.Column(db.Numeric(precision=10, scale=2))
    Change = db.Column(db.Integer)
    Volume = db.Column(db.Integer)
    TodaysMax = db.Column(db.Numeric(precision=10, scale=2))
    TodaysMin = db.Column(db.Numeric(precision=10, scale=2))
    PreviousClose = db.Column(db.Numeric(precision=10, scale=2))
    IndustryName = db.Column(db.String(100), db.ForeignKey('industries.IndustryName'))
    StockType = db.Column(db.String(100), db.ForeignKey('stocks.StockType'))
    Yield = db.Column(db.Numeric(precision=10, scale=2))
    CurrentOpinion = db.Column(db.Integer)
    CurrentOpinionWord = db.Column(db.String(50))
    Parent = db.Column(db.String(100))
    Founder = db.Column(db.String(100))
    CEO = db.Column(db.String(100))
    OneYearTarget = db.Column(db.Numeric(precision=10, scale=2))
    MaxInTotal = db.Column(db.Numeric(precision=10, scale=2))
    PredictedPriceChange = db.Column(db.String(100))
    PriceChangeDirection = db.Column(db.Integer)
    Graph_1d = db.Column(db.BLOB)
    Graph_5d = db.Column(db.BLOB)
    Graph_1m = db.Column(db.BLOB)
    Graph_6m = db.Column(db.BLOB)
    Graph_1y = db.Column(db.BLOB)
    PriceDay1 = db.Column(db.Numeric(precision=10, scale=2))
    PriceDay2 = db.Column(db.Numeric(precision=10, scale=2))
    PriceDay3 = db.Column(db.Numeric(precision=10, scale=2))
    PriceDay4 = db.Column(db.Numeric(precision=10, scale=2))
    PriceDay5 = db.Column(db.Numeric(precision=10, scale=2))
    PriceDay6 = db.Column(db.Numeric(precision=10, scale=2))
    PriceDay7 = db.Column(db.Numeric(precision=10, scale=2))
    PriceDay8 = db.Column(db.Numeric(precision=10, scale=2))
    PriceDay9 = db.Column(db.Numeric(precision=10, scale=2))
    PriceDay10 = db.Column(db.Numeric(precision=10, scale=2))
    PriceDay11 = db.Column(db.Numeric(precision=10, scale=2))
    PriceDay12 = db.Column(db.Numeric(precision=10, scale=2))
    PriceDay13 = db.Column(db.Numeric(precision=10, scale=2))
    PriceDay14 = db.Column(db.Numeric(precision=10, scale=2))
    PriceDay15 = db.Column(db.Numeric(precision=10, scale=2))
    PriceDay16 = db.Column(db.Numeric(precision=10, scale=2))
    PriceDay17 = db.Column(db.Numeric(precision=10, scale=2))
    PriceDay18 = db.Column(db.Numeric(precision=10, scale=2))
    PriceDay19 = db.Column(db.Numeric(precision=10, scale=2))
    PriceDay20 = db.Column(db.Numeric(precision=10, scale=2))
    PriceDay21 = db.Column(db.Numeric(precision=10, scale=2))
    PriceDay22 = db.Column(db.Numeric(precision=10, scale=2))
    PriceDay23 = db.Column(db.Numeric(precision=10, scale=2))
    PriceDay24 = db.Column(db.Numeric(precision=10, scale=2))
    PriceDay25 = db.Column(db.Numeric(precision=10, scale=2))
    PriceDay26 = db.Column(db.Numeric(precision=10, scale=2))
    PriceDay27 = db.Column(db.Numeric(precision=10, scale=2))
    PriceDay28 = db.Column(db.Numeric(precision=10, scale=2))
    PriceDay29 = db.Column(db.Numeric(precision=10, scale=2))
    PriceDay30 = db.Column(db.Numeric(precision=10, scale=2))

    PriceHour9 = db.Column(db.Numeric(precision=10, scale=2))
    PriceHour10 = db.Column(db.Numeric(precision=10, scale=2))
    PriceHour11 = db.Column(db.Numeric(precision=10, scale=2))
    PriceHour12 = db.Column(db.Numeric(precision=10, scale=2))
    PriceHour13 = db.Column(db.Numeric(precision=10, scale=2))
    PriceHour14 = db.Column(db.Numeric(precision=10, scale=2))
    PriceHour15 = db.Column(db.Numeric(precision=10, scale=2))

    def __init__(self, Name, Logo, StockName, CurrentPrice, LastChange, PercentChange, Change, Volume, TodaysMax, TodaysMin, PreviousClose, IndustryName, StockType, Yield, CurrentOpinion, CurrentOpinionWord, Parent, Founder, CEO, OneYearTarget, MaxInTotal, PredictedPriceChange, PriceChangeDirection, Graph_1d, Graph_5d, Graph_1m, Graph_6m, Graph_1y, PriceDay1, PriceDay2, PriceDay3, PriceDay4, PriceDay5, PriceDay6, PriceDay7, PriceDay8, PriceDay9, PriceDay10, PriceDay11, PriceDay12, PriceDay13, PriceDay14, PriceDay15, PriceDay16, PriceDay17, PriceDay18, PriceDay19, PriceDay20, PriceDay21, PriceDay22, PriceDay23, PriceDay24, PriceDay25, PriceDay26, PriceDay27, PriceDay28, PriceDay29, PriceDay30,  PriceHour9, PriceHour10, PriceHour11, PriceHour12, PriceHour13, PriceHour14, PriceHour15):
        self.Name = Name
        self.Logo = Logo
        self.StockName = StockName
        self.CurrentPrice = CurrentPrice
        self.LastChange = LastChange
        self.PercentChange = PercentChange
        self.Change = Change
        self.Volume = Volume
        self.TodaysMax = TodaysMax
        self.TodaysMin = TodaysMin
        self.PreviousClose = PreviousClose
        self.IndustryName = IndustryName
        self.StockType = StockType
        self.Yield = Yield
        self.CurrentOpinion = CurrentOpinion
        self.CurrentOpinionWord = CurrentOpinionWord
        self.Parent = Parent
        self.Founder = Founder
        self.CEO = CEO
        self.OneYearTarget = OneYearTarget
        self.MaxInTotal = MaxInTotal
        self.PredictedPriceChange = PredictedPriceChange
        self.PriceChangeDirection = PriceChangeDirection
        self.Graph_1d = Graph_1d
        self.Graph_5d = Graph_5d
        self.Graph_1m = Graph_1m
        self.Graph_6m = Graph_6m
        self.Graph_1y = Graph_1y
        self.PriceDay1 = PriceDay1
        self.PriceDay2 = PriceDay2
        self.PriceDay3 = PriceDay3
        self.PriceDay4 = PriceDay4
        self.PriceDay5 = PriceDay5
        self.PriceDay6 = PriceDay6
        self.PriceDay7 = PriceDay7
        self.PriceDay8 = PriceDay8
        self.PriceDay9 = PriceDay9
        self.PriceDay10 = PriceDay10
        self.PriceDay11 = PriceDay11
        self.PriceDay12 = PriceDay12
        self.PriceDay13 = PriceDay13
        self.PriceDay14 = PriceDay14
        self.PriceDay15 = PriceDay15
        self.PriceDay16 = PriceDay16
        self.PriceDay17 = PriceDay17
        self.PriceDay18 = PriceDay18
        self.PriceDay19 = PriceDay19
        self.PriceDay20 = PriceDay20
        self.PriceDay21 = PriceDay21
        self.PriceDay22 = PriceDay22
        self.PriceDay23 = PriceDay23
        self.PriceDay24 = PriceDay24
        self.PriceDay25 = PriceDay25
        self.PriceDay26 = PriceDay26
        self.PriceDay27 = PriceDay27
        self.PriceDay28 = PriceDay28
        self.PriceDay29 = PriceDay29
        self.PriceDay30 = PriceDay30
        
        self.PriceHour9 = PriceHour9
        self.PriceHour10 = PriceHour10
        self.PriceHour11 = PriceHour11
        self.PriceHour12 = PriceHour12
        self.PriceHour13 = PriceHour13
        self.PriceHour14 = PriceHour14
        self.PriceHour15 = PriceHour15

class Followed(db.Model):
    __tablename__='followed'
    CompanyID = db.Column(db.Integer, db.ForeignKey('companies.CompanyID'), primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    def __init__(self, CompanyID, UserID):
        self.CompanyID = CompanyID
        self.UserID = UserID

class Suggested(db.Model):
    __tablename__='suggested'
    CompanyID = db.Column(db.Integer, db.ForeignKey('companies.CompanyID'), primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    SuggestMetric = db.Column(db.Integer)

    def __init__(self, CompanyID, UserID, SuggestMetric):
        self.CompanyID = CompanyID
        self.UserID = UserID
        self.SuggestMetric = SuggestMetric

class News(db.Model):
    __tablename__='news'
    NewsID = db.Column(db.Integer, primary_key=True)
    Headline = db.Column(db.String(100), nullable=False)
    Photo = db.Column(db.String(100))
    SourceName = db.Column(db.String(100))
    SourceURL = db.Column(db.String(100))
    OutlookMetric = db.Column(db.Integer)
    CompanyID = db.Column(db.Integer, db.ForeignKey('companies.CompanyID'))
    Timestamp = db.Column(db.String(100))

    def __init__(self, Headline, Photo, SourceName, SourceURL, OutlookMetric, CompanyID, Timestamp):
        self.Headline = Headline
        self.Photo = Photo
        self.SourceName = SourceName
        self.SourceURL = SourceURL
        self.OutlookMetric = OutlookMetric
        self.CompanyID = CompanyID
        self.Timestamp = Timestamp

class Notifications(db.Model):
    __tablename__='notifications'
    NewsID = db.Column(db.Integer, db.ForeignKey('news.NewsID'), primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    CompanyID = db.Column(db.Integer, db.ForeignKey('companies.CompanyID'), primary_key=True)
    Read = db.Column(db.Integer)
    Timestamp = db.Column(db.String(100))
 
    def __init__ (self, NewsID, UserID, CompanyID, Read, Timestamp):
        self.NewsID = NewsID
        self.UserID = UserID
        self.CompanyID = CompanyID
        self.Read = Read
        self.Timestamp = Timestamp



import base64
import os

from base64 import b64encode

from datetime import datetime
from datetime import date
from datetime import time
import time

def dbinit():
    
    with open('src/static/images/userpng.jpg', 'rb') as file:
        image_data3 = file.read()

    
    sample_users = [
        Users(FirstName='John', LastName='Doe', Username='john_doe', Password='password123', ProfilePic=image_data3),
        Users(FirstName='Alice', LastName='Smith', Username='alice_smith', Password='abc123', ProfilePic=image_data3),
        Users(FirstName='Bob', LastName='Johnson', Username='bob_johnson', Password='securepass', ProfilePic=image_data3),
        Users(FirstName='Emily', LastName='Brown', Username='emily_brown', Password='emily123', ProfilePic=image_data3),
        Users(FirstName='Michael', LastName='Davis', Username='michael_davis', Password='mikepass', ProfilePic=image_data3)
    ]

    for user in sample_users:
        db.session.add(user)

    db.session.commit()
    
    sample_industry_preferences = [
        IndustryPreferences(User_ID=1, IndustryName='Technology'),
        IndustryPreferences(User_ID=2, IndustryName='Finance'),
        IndustryPreferences(User_ID=3, IndustryName='Healthcare'),
        IndustryPreferences(User_ID=4, IndustryName='Retail'),
        IndustryPreferences(User_ID=5, IndustryName='Energy')
    ]

    sample_industries = [
        Industry(IndustryName='Technology'),
        Industry(IndustryName='Finance'),
        Industry(IndustryName='Healthcare'),
        Industry(IndustryName='Retail'),
        Industry(IndustryName='Energy')
    ]

    sample_stock_preferences = [
        StockPreferences(User_ID=1, StockType='Stable'),
        StockPreferences(User_ID=2, StockType='Volatile'),
        StockPreferences(User_ID=3, StockType='Blue Chip'),
        StockPreferences(User_ID=4, StockType='Mutual Fund'),
        StockPreferences(User_ID=5, StockType='Bonds')
    ]

    sample_stocks = [
        Stocks(StockType='Stable'),
        Stocks(StockType='Volatile'),
        Stocks(StockType='Blue Chip'),
        Stocks(StockType='Mutual Fund'),
        Stocks(StockType='Bonds')
    ]

    for entry in sample_industry_preferences + sample_industries + sample_stock_preferences + sample_stocks:
        db.session.add(entry)

    db.session.commit()
    
    
    with open('src/static/images/sample_logo.webp', 'rb') as file:
        image_data = file.read()

    img = base64.b64encode(image_data).decode('utf-8')
    
    
    # Create sample entries
    sample_companies = [
        # Companies(
        #     Name='Company1',
        #     Logo=image_data,
        #     StockName='COMP1',
        #     CurrentPrice=100.00,
        #     LastChange='+2',
        #     PercentChange = 10.50,
        #     Change=1,
        #     Volume=1000,
        #     TodaysMax=110.00,
        #     TodaysMin=90.00,
        #     PreviousClose=95.00,
        #     IndustryName='Technology',
        #     StockType='Stable',
        #     Yield=0.05,
        #     CurrentOpinion=2,
        #     CurrentOpinionWord='Very Positive',
        #     Parent='Parent1',
        #     Founder='Founder1',
        #     CEO='CEO1',
        #     OneYearTarget=120.00,
        #     MaxInTotal=200.00,
        #     PredictedPriceChange='+ $3.50 (10%)',
        #     PriceChangeDirection=1,
        #     Graph_1d=None,  # Blob data for graphs
        #     Graph_5d=None,
        #     Graph_1m=None,
        #     Graph_6m=None,
        #     Graph_1y=None,
        #     PriceDay1=100.00,  
        #     PriceDay2=102.00,
        #     PriceDay3=102.00,
        #     PriceDay4=102.00,
        #     PriceDay5=102.00,
        #     PriceDay6=100.00,  
        #     PriceDay7=102.00,
        #     PriceDay8=102.00,
        #     PriceDay9=102.00,
        #     PriceDay10=102.00,
        #     PriceDay11=100.00,  
        #     PriceDay12=102.00,
        #     PriceDay13=102.00,
        #     PriceDay14=102.00,
        #     PriceDay15=102.00,
        #     PriceDay16=100.00,  
        #     PriceDay17=102.00,
        #     PriceDay18=102.00,
        #     PriceDay19=102.00,
        #     PriceDay20=102.00,
        #     PriceDay21=100.00,  
        #     PriceDay22=102.00,
        #     PriceDay23=102.00,
        #     PriceDay24=102.00,
        #     PriceDay25=102.00,
        #     PriceDay26=100.00,  
        #     PriceDay27=102.00,
        #     PriceDay28=102.00,
        #     PriceDay29=102.00,
        #     PriceDay30=102.00,
        #     # Prices for each hour (from 9:00 AM to 3:00 PM)
        #     PriceHour9=101.00,
        #     PriceHour10=102.00,
        #     PriceHour11=103.00,
        #     PriceHour12=104.00,
        #     PriceHour13=105.00,
        #     PriceHour14=106.00,
        #     PriceHour15=107.00
        # ),
        # Companies(
        #     Name='Company2',
        #     Logo=image_data,
        #     StockName='COMP2',
        #     CurrentPrice=110.00,
        #     LastChange='-2',
        #     PercentChange = -10.50,
        #     Change=-1,
        #     Volume=1200,
        #     TodaysMax=115.00,
        #     TodaysMin=105.00,
        #     PreviousClose=107.00,
        #     IndustryName='Finance',
        #     StockType='Blue Chip',
        #     Yield=0.04,
        #     CurrentOpinion=1,
        #     CurrentOpinionWord='Slightly Positive',
        #     Parent='Parent2',
        #     Founder='Founder2',
        #     CEO='CEO2',
        #     OneYearTarget=125.00,
        #     MaxInTotal=250.00,
        #     PredictedPriceChange='+ $3.50 (10%)',
        #     PriceChangeDirection=1,
        #     Graph_1d=None,
        #     Graph_5d=None,
        #     Graph_1m=None,
        #     Graph_6m=None,
        #     Graph_1y=None,
        #     PriceDay1=100.00,  
        #     PriceDay2=102.00,
        #     PriceDay3=102.00,
        #     PriceDay4=102.00,
        #     PriceDay5=102.00,
        #     PriceDay6=100.00,  
        #     PriceDay7=102.00,
        #     PriceDay8=102.00,
        #     PriceDay9=102.00,
        #     PriceDay10=102.00,
        #     PriceDay11=100.00,  
        #     PriceDay12=102.00,
        #     PriceDay13=102.00,
        #     PriceDay14=102.00,
        #     PriceDay15=102.00,
        #     PriceDay16=100.00,  
        #     PriceDay17=102.00,
        #     PriceDay18=102.00,
        #     PriceDay19=102.00,
        #     PriceDay20=102.00,
        #     PriceDay21=100.00,  
        #     PriceDay22=102.00,
        #     PriceDay23=102.00,
        #     PriceDay24=102.00,
        #     PriceDay25=102.00,
        #     PriceDay26=100.00,  
        #     PriceDay27=102.00,
        #     PriceDay28=102.00,
        #     PriceDay29=102.00,
        #     PriceDay30=102.00,
        #     PriceHour9=111.00,
        #     PriceHour10=112.00,
        #     PriceHour11=113.00,
        #     PriceHour12=114.00,
        #     PriceHour13=115.00,
        #     PriceHour14=116.00,
        #     PriceHour15=117.00
        # ),
        # Companies(
        #     Name='Company3',
        #     Logo=image_data,
        #     StockName='COMP3',
        #     CurrentPrice=110.00,
        #     LastChange='-2',
        #     PercentChange = -10.50,
        #     Change=-1,
        #     Volume=1200,
        #     TodaysMax=115.00,
        #     TodaysMin=105.00,
        #     PreviousClose=107.00,
        #     IndustryName='Finance',
        #     StockType='Blue Chip',
        #     Yield=0.04,
        #     CurrentOpinion=0,
        #     CurrentOpinionWord='Average',
        #     Parent='Parent2',
        #     Founder='Founder2',
        #     CEO='CEO2',
        #     OneYearTarget=125.00,
        #     MaxInTotal=250.00,
        #     PredictedPriceChange='+ $3.50 (10%)',
        #     PriceChangeDirection=1,
        #     Graph_1d=None,
        #     Graph_5d=None,
        #     Graph_1m=None,
        #     Graph_6m=None,
        #     Graph_1y=None,
        #     PriceDay1=100.00,  
        #     PriceDay2=102.00,
        #     PriceDay3=102.00,
        #     PriceDay4=102.00,
        #     PriceDay5=102.00,
        #     PriceDay6=100.00,  
        #     PriceDay7=102.00,
        #     PriceDay8=102.00,
        #     PriceDay9=102.00,
        #     PriceDay10=102.00,
        #     PriceDay11=100.00,  
        #     PriceDay12=102.00,
        #     PriceDay13=102.00,
        #     PriceDay14=102.00,
        #     PriceDay15=102.00,
        #     PriceDay16=100.00,  
        #     PriceDay17=102.00,
        #     PriceDay18=102.00,
        #     PriceDay19=102.00,
        #     PriceDay20=102.00,
        #     PriceDay21=100.00,  
        #     PriceDay22=102.00,
        #     PriceDay23=102.00,
        #     PriceDay24=102.00,
        #     PriceDay25=102.00,
        #     PriceDay26=100.00,  
        #     PriceDay27=102.00,
        #     PriceDay28=102.00,
        #     PriceDay29=102.00,
        #     PriceDay30=102.00,
        #     PriceHour9=111.00,
        #     PriceHour10=112.00,
        #     PriceHour11=113.00,
        #     PriceHour12=114.00,
        #     PriceHour13=115.00,
        #     PriceHour14=116.00,
        #     PriceHour15=117.00
        # ),
        # Companies(
        #     Name='Company4',
        #     Logo=image_data,
        #     StockName='COMP4',
        #     CurrentPrice=110.00,
        #     LastChange='-2',
        #     PercentChange = -10.50,
        #     Change=-1,
        #     Volume=1200,
        #     TodaysMax=115.00,
        #     TodaysMin=105.00,
        #     PreviousClose=107.00,
        #     IndustryName='Finance',
        #     StockType='Bonds',
        #     Yield=0.04,
        #     CurrentOpinion=-1,
        #     CurrentOpinionWord='Slightly Negative',
        #     Parent='Parent2',
        #     Founder='Founder2',
        #     CEO='CEO2',
        #     OneYearTarget=125.00,
        #     MaxInTotal=250.00,
        #     PredictedPriceChange='+ $3.50 (10%)',
        #     PriceChangeDirection=1,
        #     Graph_1d=None,
        #     Graph_5d=None,
        #     Graph_1m=None,
        #     Graph_6m=None,
        #     Graph_1y=None,
        #     PriceDay1=100.00,  
        #     PriceDay2=102.00,
        #     PriceDay3=102.00,
        #     PriceDay4=102.00,
        #     PriceDay5=102.00,
        #     PriceDay6=100.00,  
        #     PriceDay7=102.00,
        #     PriceDay8=102.00,
        #     PriceDay9=102.00,
        #     PriceDay10=102.00,
        #     PriceDay11=100.00,  
        #     PriceDay12=102.00,
        #     PriceDay13=102.00,
        #     PriceDay14=102.00,
        #     PriceDay15=102.00,
        #     PriceDay16=100.00,  
        #     PriceDay17=102.00,
        #     PriceDay18=102.00,
        #     PriceDay19=102.00,
        #     PriceDay20=102.00,
        #     PriceDay21=100.00,  
        #     PriceDay22=102.00,
        #     PriceDay23=102.00,
        #     PriceDay24=102.00,
        #     PriceDay25=102.00,
        #     PriceDay26=100.00,  
        #     PriceDay27=102.00,
        #     PriceDay28=102.00,
        #     PriceDay29=102.00,
        #     PriceDay30=102.00,
        #     PriceHour9=111.00,
        #     PriceHour10=112.00,
        #     PriceHour11=113.00,
        #     PriceHour12=114.00,
        #     PriceHour13=115.00,
        #     PriceHour14=116.00,
        #     PriceHour15=117.00
        # ),
        # Companies(
        #     Name='Company5',
        #     Logo=image_data,
        #     StockName='COMP5',
        #     CurrentPrice=110.00,
        #     LastChange='+2',
        #     PercentChange = 10.50,
        #     Change=1,
        #     Volume=1200,
        #     TodaysMax=115.00,
        #     TodaysMin=105.00,
        #     PreviousClose=107.00,
        #     IndustryName='Finance',
        #     StockType='Blue Chip',
        #     Yield=0.04,
        #     CurrentOpinion=-2,
        #     CurrentOpinionWord='Very Negative',
        #     Parent='Parent2',
        #     Founder='Founder2',
        #     CEO='CEO2',
        #     OneYearTarget=125.00,
        #     MaxInTotal=250.00,
        #     PredictedPriceChange='+ $3.50 (10%)',
        #     PriceChangeDirection=1,
        #     Graph_1d=None,
        #     Graph_5d=None,
        #     Graph_1m=None,
        #     Graph_6m=None,
        #     Graph_1y=None,
        #     PriceDay1=100.00,  
        #     PriceDay2=102.00,
        #     PriceDay3=102.00,
        #     PriceDay4=102.00,
        #     PriceDay5=102.00,
        #     PriceDay6=100.00,  
        #     PriceDay7=102.00,
        #     PriceDay8=102.00,
        #     PriceDay9=102.00,
        #     PriceDay10=102.00,
        #     PriceDay11=100.00,  
        #     PriceDay12=102.00,
        #     PriceDay13=102.00,
        #     PriceDay14=102.00,
        #     PriceDay15=102.00,
        #     PriceDay16=100.00,  
        #     PriceDay17=102.00,
        #     PriceDay18=102.00,
        #     PriceDay19=102.00,
        #     PriceDay20=102.00,
        #     PriceDay21=100.00,  
        #     PriceDay22=102.00,
        #     PriceDay23=102.00,
        #     PriceDay24=102.00,
        #     PriceDay25=102.00,
        #     PriceDay26=100.00,  
        #     PriceDay27=102.00,
        #     PriceDay28=102.00,
        #     PriceDay29=102.00,
        #     PriceDay30=102.00,
        #     PriceHour9=111.00,
        #     PriceHour10=112.00,
        #     PriceHour11=113.00,
        #     PriceHour12=114.00,
        #     PriceHour13=115.00,
        #     PriceHour14=116.00,
        #     PriceHour15=117.00
        # )
    ]

    for company in sample_companies:
        db.session.add(company)

    db.session.commit()  
    
    followed_samples = [
        Followed(CompanyID=1, UserID=1),
        Followed(CompanyID=2, UserID=1),
        Followed(CompanyID=3, UserID=2),
        Followed(CompanyID=4, UserID=3),
        Followed(CompanyID=5, UserID=3)
    ]
    
    suggested_samples = [
        Suggested(CompanyID=1, UserID=1, SuggestMetric=8),
        Suggested(CompanyID=2, UserID=1, SuggestMetric=7),
        Suggested(CompanyID=3, UserID=2, SuggestMetric=6),
        Suggested(CompanyID=4, UserID=3, SuggestMetric=5),
        Suggested(CompanyID=5, UserID=3, SuggestMetric=9)
    ]
    
    with open('src/static/images/stockmarket.webp', 'rb') as file2:
        image_data2 = file2.read()

    img = base64.b64encode(image_data).decode('utf-8')
    
    news_samples = [
        News(Headline='Company 1 releases new product', Photo=image_data, SourceName='Tech News', SourceURL='https://technews.com', OutlookMetric=1, CompanyID=1, Timestamp=datetime.now()),
        News(Headline='Company 2 reports record profits', Photo=image_data2, SourceName='Finance Times', SourceURL='https://financetimes.com', OutlookMetric=1, CompanyID=2, Timestamp=datetime.now()),
        News(Headline='Company 3 faces lawsuit', Photo=image_data2, SourceName='Legal News', SourceURL='https://legalnews.com', OutlookMetric=-1, CompanyID=1, Timestamp=datetime.now()),
        News(Headline='Company 4 announces merger', Photo=image_data2, SourceName='Business Insider', SourceURL='https://businessinsider.com', OutlookMetric=-1, CompanyID=1, Timestamp=datetime.now()),
        News(Headline='Company 5 launches new marketing campaign', Photo=image_data2, SourceName='Marketing Weekly', SourceURL='https://marketingweekly.com', OutlookMetric=1, CompanyID=2, Timestamp=datetime.now())
    ]
    
    notifications_samples = [
        Notifications(NewsID=1, UserID=1, CompanyID=1, Read=0, Timestamp=datetime.now()),
        Notifications(NewsID=2, UserID=1, CompanyID=1, Read=0, Timestamp=datetime.now()),
        Notifications(NewsID=3, UserID=1, CompanyID=1, Read=0, Timestamp=datetime.now()),
        Notifications(NewsID=2, UserID=1, CompanyID=2, Read=1, Timestamp=datetime.now()),
        Notifications(NewsID=3, UserID=2, CompanyID=3, Read=0, Timestamp=datetime.now()),
        Notifications(NewsID=4, UserID=3, CompanyID=4, Read=1, Timestamp=datetime.now()),
        Notifications(NewsID=5, UserID=3, CompanyID=5, Read=0, Timestamp=datetime.now())
    ]

    for company in suggested_samples:
        db.session.add(company)
        
    for company in followed_samples:
        db.session.add(company)
        
    for company in news_samples:
        db.session.add(company)
        
    for company in notifications_samples:
        db.session.add(company)

    db.session.commit()        