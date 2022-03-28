import requests
from datetime import date, timedelta
from config import *
import os
from twilio.rest import Client

xSTOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
stock_parameters = {'function': 'TIME_SERIES_Daily', 'symbol': xSTOCK, 'interval': '5min', 'apikey': STOCK_API_KEY}
news_parameters = {'qInTitle': 'tesla', 'from': '2022-02-18', 'sortBy': 'publishedAt', 'language': 'en',
                   'apiKey': NEWS_API_KEY}

client = Client(account_sid, auth_token)


def get_change(current, previous):
    if current == previous:
        return 100.0
    try:
        return (abs(current - previous) / previous) * 100.0
    except ZeroDivisionError:
        return 0


news_response = requests.get(NEWS_ENDPOINT, params=news_parameters)
news_response.raise_for_status()
news_data = news_response.json()

stock_response = requests.get(STOCK_ENDPOINT, params=stock_parameters)
stock_response.raise_for_status()
stock_data = stock_response.json()

today = date.today()
yesterday = today - timedelta(days=1)
day_before_yesterday = today - timedelta(days=2)

yesterdays_close = stock_data['Time Series (Daily)'][str(yesterday)]['4. close']
day_before_yesterday_close = stock_data['Time Series (Daily)'][str(day_before_yesterday)]['4. close']

headlines = []
briefs = []
percentage = get_change(float(yesterdays_close), float(day_before_yesterday_close))

for num in range(3):
    headlines.append(news_data['articles'][num]['title'])
for num in range(3):
    briefs.append(news_data['articles'][num]['description'])


for num in range(3):
    if yesterdays_close > day_before_yesterday_close:
        message = client.messages \
            .create(
            body=f'TSLA: 🔺{int(percentage)}'
                 f'\nHeadline:{headlines[num]}'
                 f'\nBrief:{briefs[num]}',
            from_='12283007476',
            to='13473306396'

        )

    elif yesterdays_close < day_before_yesterday_close:
        message = client.messages \
            .create(
            body=f'TSLA: 🔻{int(percentage)}'
                 f'\nHeadline:{headlines[num]},'
                 f'\nBrief:{briefs[num]}',
            from_='Your Twillio number',
            to= 'Your Twillio approved number'
        )

    else:
        print('No Change')

print(message.status)
