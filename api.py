import datetime
import json
import math
import os
import time

# from tqdm import tqdm
from pprint import pprint

import numpy as np
import pandas as pd
import requests
import yfinance as yf
from dotenv import load_dotenv
from ratelimit import limits, sleep_and_retry

# from dateutil.tz import tzutc

load_dotenv()
APPLICATION_ID = os.getenv("APPLICATION_ID")
APPLICATION_KEY = os.getenv("APPLICATION_KEY")
APPLICATION_USERNAME = os.getenv("APPLICATION_USERNAME")
APPLICATION_PASSWORD = os.getenv("APPLICATION_PASSWORD")
tickers = pd.read_csv("./data/sp500wiki.csv")
headers = {
    "X-AYLIEN-NewsAPI-Application-ID": APPLICATION_ID,
    "X-AYLIEN-NewsAPI-Application-Key": APPLICATION_KEY,
}
token = requests.post(
    "https://api.aylien.com/v1/oauth/token",
    auth=(APPLICATION_USERNAME, APPLICATION_PASSWORD),
    data={"grant_type": "password"},
).json()["access_token"]
headers = {"Authorization": "Bearer {}".format(token), "AppId": APPLICATION_ID}

COLS = [
    "Symbol",
    "Volume",
    "GICS Sector",
    "GICS Sub-Industry",
    "News - Volume",
    "News - Positive Sentiment",
    "News - Negative Sentiment",
    "News - New Products",
    "News - Layoffs",
    "News - Analyst Comments",
    "News - Stocks",
    "News - Dividends",
    "News - Corporate Earnings",
    "News - Mergers & Acquisitions",
    "News - Store Openings",
    "News - Product Recalls",
    "News - Adverse Events",
    "News - Personnel Changes",
    "News - Stock Rumors",
]


def get_urls(symbol):
    return {
        f'https://api.aylien.com/v6/news/stories?aql=language:(en) AND entities:({{{{surface_forms.text:"{symbol}" AND overall_prominence:>=0.65}}}})&cursor=*&published_at.end=NOW&published_at.start=NOW-1DAYS/DAY': "News - Volume",
        f'https://api.aylien.com/v6/news/stories?aql=language:(en) AND entities:({{{{surface_forms.text:"{symbol}" AND overall_prominence:>=0.65 AND sentiment:positive}}}})&cursor=*&published_at.end=NOW&published_at.start=NOW-1DAYS/DAY': "News - Positive Sentiment",
        f'https://api.aylien.com/v6/news/stories?aql=language:(en) AND entities:({{{{surface_forms.text:"{symbol}" AND overall_prominence:>=0.65 AND sentiment:negative}}}})&cursor=*&published_at.end=NOW&published_at.start=NOW-1DAYS/DAY': "News - Negative Sentiment",
        f'https://api.aylien.com/v6/news/stories?aql=language:(en) AND categories:({{{{taxonomy:aylien AND id:ay.biz.newprod}}}}) AND entities:({{{{surface_forms.text:"{symbol}" AND overall_prominence:>=0.65}}}})&cursor=*&published_at.end=NOW&published_at.start=NOW-1DAYS/DAY': "News - New Products",
        f'https://api.aylien.com/v6/news/stories?aql=language:(en) AND categories:({{{{taxonomy:aylien AND id:ay.biz.layoffs}}}}) AND entities:({{{{surface_forms.text:"{symbol}" AND overall_prominence:>=0.65}}}})&cursor=*&published_at.end=NOW&published_at.start=NOW-1DAYS/DAY': "News - Layoffs",
        f'https://api.aylien.com/v6/news/stories?aql=language:(en) AND categories:({{{{taxonomy:aylien AND id:ay.fin.analyst}}}}) AND entities:({{{{surface_forms.text:"{symbol}" AND overall_prominence:>=0.65}}}})&cursor=*&published_at.end=NOW&published_at.start=NOW-1DAYS/DAY': "News - Analyst Comments",
        f'https://api.aylien.com/v6/news/stories?aql=language:(en) AND categories:({{{{taxonomy:aylien AND id:ay.fin.stocks}}}}) AND entities:({{{{surface_forms.text:"{symbol}" AND overall_prominence:>=0.65}}}})&cursor=*&published_at.end=NOW&published_at.start=NOW-1DAYS/DAY': "News - Stocks",
        f'https://api.aylien.com/v6/news/stories?aql=language:(en) AND categories:({{{{taxonomy:aylien AND id:ay.biz.dividend}}}}) AND entities:({{{{surface_forms.text:"{symbol}" AND overall_prominence:>=0.65}}}})&cursor=*&published_at.end=NOW&published_at.start=NOW-1DAYS/DAY': "News - Dividends",
        f'https://api.aylien.com/v6/news/stories?aql=language:(en) AND categories:({{{{taxonomy:aylien AND id:ay.fin.reports}}}}) AND entities:({{{{surface_forms.text:"{symbol}" AND overall_prominence:>=0.65}}}})&cursor=*&published_at.end=NOW&published_at.start=NOW-1DAYS/DAY': "News - Corporate Earnings",
        f'https://api.aylien.com/v6/news/stories?aql=language:(en) AND categories:({{{{taxonomy:aylien AND id:ay.biz.manda}}}}) AND entities:({{{{surface_forms.text:"{symbol}" AND overall_prominence:>=0.65}}}})&cursor=*&published_at.end=NOW&published_at.start=NOW-1DAYS/DAY': "News - Mergers & Acquisitions",
        f'https://api.aylien.com/v6/news/stories?aql=language:(en) AND categories:({{{{taxonomy:aylien AND id:ay.biz.expand}}}}) AND entities:({{{{surface_forms.text:"{symbol}" AND overall_prominence:>=0.65}}}})&cursor=*&published_at.end=NOW&published_at.start=NOW-1DAYS/DAY': "News - Store Openings",
        f'https://api.aylien.com/v6/news/stories?aql=language:(en) AND categories:({{{{taxonomy:aylien AND id:ay.biz.recall}}}}) AND entities:({{{{surface_forms.text:"{symbol}" AND overall_prominence:>=0.65}}}})&cursor=*&published_at.end=NOW&published_at.start=NOW-1DAYS/DAY': "News - Product Recalls",
        f'https://api.aylien.com/v6/news/stories?aql=language:(en) AND categories:({{{{taxonomy:aylien AND id:ay.spec.adverse}}}}) AND entities:({{{{surface_forms.text:"{symbol}" AND overall_prominence:>=0.65}}}})&cursor=*&published_at.end=NOW&published_at.start=NOW-1DAYS/DAY': "News - Adverse Events",
        f'https://api.aylien.com/v6/news/stories?aql=language:(en) AND categories:({{{{taxonomy:aylien AND id:ay.biz.persmove}}}}) AND entities:({{{{surface_forms.text:"{symbol}" AND overall_prominence:>=0.65}}}})&cursor=*&published_at.end=NOW&published_at.start=NOW-1DAYS/DAY': "News - Personnel Changes",
        f'https://api.aylien.com/v6/news/stories?aql=language:(en) AND categories:({{{{taxonomy:aylien AND id:ay.fin.rumor}}}}) AND entities:({{{{surface_forms.text:"{symbol}" AND overall_prominence:>=0.65}}}})&cursor=*&published_at.end=NOW&published_at.start=NOW-1DAYS/DAY': "News - Stock Rumors",
    }


@sleep_and_retry
@limits(calls=60, period=60)
def call_api(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception("API response: {}".format(response.status_code))
    return response


def get_api(symbol: str):
    if tickers.isin([symbol]).any().any():
        data = np.zeros((1, len(COLS)))
        user_input = pd.DataFrame(data, columns=COLS)
        user_input["Symbol"] = symbol

        sp_500_info = tickers.loc[tickers["Symbol"] == symbol].iloc[0]
        user_input["GICS Sector"] = sp_500_info["GICS Sector"]
        user_input["GICS Sub-Industry"] = sp_500_info["GICS Sub-Industry"]

        urls = get_urls(symbol)
        for url, col in urls.items():
            response = call_api(url, headers=headers).json()
            user_input[col] = len(response["stories"])

        stock = yf.Ticker(symbol)
        stock_history = stock.history(period="1d")
        user_input["Volume"] = stock_history["Volume"].values
        return user_input


print(get_api("AMZN"))
