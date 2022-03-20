#/usr/bin/python3.6
# coding: utf-8

import requests
from finnhub import client as Finnhub
from pandas.io.json import json_normalize
import json
import requests
import pandas as pd
import pygsheets
import time



token = 'your_finnhub_token_here'
gc = pygsheets.authorize(service_file=r"google_spreadsheets_token_here")


# Export data to Spreadsheets
def export_to_gsheets(gsheet_id, tab_id, df):
    sh = gc.open_by_url(gsheet_id)
    wks = sh.worksheet_by_title(tab_id)
    wks.clear()
    return wks.set_dataframe(df, (1,1), nan='')


# STOCKS CANDLES WEEKLY

def get_stocks_data_weekly(symbols):
    column_names = ['c', 'h', 'l', 'o', 's', 't', 'v']
    df_all_stocks = pd.DataFrame(columns = column_names)
    for i in symbols:
        resolution = 'W'
        count_days = 104
        r = requests.get('https://finnhub.io/api/v1/stock/candle?symbol={0}&resolution={1}&count={2}&token={3}'.format(i, resolution, count_days, token))
        p = r.json()
        df_candels = pd.read_json(json.dumps(p))
        try:
            df_candels['t'] = pd.to_datetime(df_candels['t'], unit='s')
            df_candels['symbol'] = i
        except:
            pass
        df_all_stocks = pd.concat([df_all_stocks, df_candels], sort=False)
    return df_all_stocks


# STOCKS CANDLES DAILY
def get_stocks_data_daily(symbols):
    column_names = ['c', 'h', 'l', 'o', 's', 't', 'v']
    df_all_stocks = pd.DataFrame(columns = column_names)
    for i in symbols:
        resolution = 'D'
        count_days = 100
        r = requests.get('https://finnhub.io/api/v1/stock/candle?symbol={0}&resolution={1}&count={2}&token={3}'.format(i, resolution, count_days, token))
        p = r.json()
        df_candels = pd.read_json(json.dumps(p))
        try:
            df_candels['t'] = pd.to_datetime(df_candels['t'], unit='s')
            df_candels['symbol'] = i
        except:
            pass
        df_all_stocks = pd.concat([df_all_stocks, df_candels], sort=False)
    return df_all_stocks


# RECOMMENDATIONS FROM ANALYSTS
def get_recommendations_data(symbols):
    column_names = ['symbol', 'period', 'strongBuy', 'buy', 'hold', 'sell', 'strongSell']
    df_all_recommendations = pd.DataFrame(columns = column_names)
    for i in symbols:
        r = requests.get('https://finnhub.io/api/v1/stock/recommendation?symbol={0}&token={1}'.format(i, token))
        p = r.json()
        df_recommendation = pd.read_json(json.dumps(p))
        try:
            df_recommendation = df_recommendation.loc[:, ['symbol', 'period', 'strongBuy', 'buy', 'hold', 'sell', 'strongSell']]
        except:
            pass
        df_all_recommendations = pd.concat([df_all_recommendations, df_recommendation], sort=False)
    return df_all_recommendations

# Company news
def get_company_news(symbols):
    column_names = ['category', 'datetime', 'headline', 'id', 'image', 'related', 'source', 'summary', 'url', 'symbol']
    df_all_news = pd.DataFrame(columns = column_names)
    for i in symbols:
        r = requests.get('https://finnhub.io/api/v1/news/{0}?token={1}'.format(i, token))
        p = r.json()
        df_news = pd.read_json(json.dumps(p))
        try:
            df_news = df_news.loc[:, ['category', 'datetime', 'headline', 'id', 'image', 'related', 'source', 'summary', 'url']]
            df_news['symbol'] = i
        except:
            pass
        df_all_news = pd.concat([df_all_news, df_news], sort=False)
    return df_all_news


# Financial Metrics - margin
def get_margin_metrics(symbols):
    metric_types = ['price', 'valuation', 'growth', 'margin', 'management', 'financialStrength', 'perShare']
    column_names = ['metric', 'value', 'metricType', 'symbol']
    df_margin_metrics_all = pd.DataFrame(columns = column_names)
    for n in metric_types:
        try:
            for i in symbols:
                r = requests.get('https://finnhub.io/api/v1/stock/metric?symbol={0}&metric={1}&token={2}'.format(i, n, token))
                p = r.json()
                df_margin_metrics = pd.read_json(json.dumps(p))
                try:
                    df_margin_metrics.reset_index(inplace=True)
                    df_margin_metrics.columns = ['metric', 'value', 'metricType', 'symbol']
                except:
                    pass
                df_margin_metrics_all = pd.concat([df_margin_metrics_all, df_margin_metrics], sort=False)
        except:
            pass
        time.sleep(60)
    return df_margin_metrics_all
