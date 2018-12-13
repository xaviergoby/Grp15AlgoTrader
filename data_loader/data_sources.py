# Author: Xavier O'Rourke Goby

import pandas_datareader as web
import pandas as pd
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from pytrends.request import TrendReq
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def get_google_trends_data(keyword, timeframe):
    """
    Requires the pytrends library
    Please visit the GitHub link for detailed explanation of the "unofficial API for Google Trends" called pytrends
    GitHub link: https://github.com/GeneralMills/pytrends
    :param keyword: a list of str format elements of the keywords to be searched
    i.e. ["Bitcoin"] or ["Debt", "Mortgage", "Financial Crisis"]
    :return: a pandas DataFrame object
    """
    pytrend_obj = TrendReq()
    pytrend_obj.build_payload(keyword, cat=0, timeframe = timeframe, geo='', gprop='')
    interest_over_time_df = pytrend_obj.interest_over_time()
    data = interest_over_time_df[keyword]
    return data

def get_stocks_data(stock_idx = "AAPL", start_date = "01/01/2004", end_date = "12/06/2018"):
    """
    Requires the pandas-datareader library
    :param stock_idx: str of yahoo index be default is "AAPL"
    :param start_date: str with format mm/dd/YYYY  (so "%m-%d-%Y") by default is "01/01/2014"
    "left end date", "oldest date"
    :param end_date: str with format mm/dd/YYY (so "%m-%d-%Y") by default is  "12/03/2018"
    "right end date", "most recent date"
    :return: A pandas.core.frame.DataFrame with cols ['Dates', 'High', 'Low', 'Open', 'Close', 'Volume', 'Adj Close']
    The index of the DataFrame is a pandas.core.indexes.datetimes.DatetimeIndex obj w/ the date stamp corresponding to
    row AKA "bar" of the table.
    The 'Dates' col is a pandas.core.series.Series type obj with it's elements being pandas._libs.tslibs.timestamps.Timestamp type objects
    """
    source = 'yahoo'
    data = web.DataReader(stock_idx,data_source=source, start=start_date, end=end_date)
    # wk_days = [d.strftime("%A") for d in data.index.date]
    datetime_dates_list = data.index.date.tolist()
    # data.insert(0, "WeekDays", wk_days)
    data.insert(0, "Dates", datetime_dates_list)
    # data.insert(0, "Dates", wk_days)
    return data

def date_transfromer(begin_date='2004-01-01',end_date=date.today(),interval='3m'):
    emptylist = []
    year = int(begin_date[0:4])
    month = int(begin_date[5:7])
    day = int(begin_date[8:10])

    datum = datetime.date(year,month,day)
    while datum < end_date:
        datum = datum + relativedelta(days=-1)
        rightformat = datum.strftime('%Y-%m-%d')
        emptylist.append(rightformat)
        # 84 is a multiple of 7
        datum = datum + relativedelta(months=+1)


    return emptylist



def multiple_time_frames_combiner(keyword,begin_date='2004-01-01',end_date=date.today()):
    date_list_3m = date_transfromer(begin_date=begin_date,end_date=end_date,interval='3m')
    date_number = 0
    google_data_frame_3_months = pd.DataFrame()
    while date_number < len(date_list_3m) -1:
        start_date = date_list_3m[date_number]
        final_date = date_list_3m[date_number + 1]
        timeframe = '{} {}'.format(start_date, final_date)
        google_data = get_google_trends_data(keyword,timeframe)
        frames = [google_data_frame_3_months,google_data]
        google_data_frame_3_months = pd.concat(frames)
        date_number += 1
    return google_data_frame_3_months

def relative_search_density_longer_period(keyword,begin_date='2004-01-01',end_date=date.today()):
    timeframe = '{} {}'.format(begin_date, end_date)
    # This has a 7-day interval
    big_picture = get_google_trends_data(keyword,timeframe)
    daily_data = multiple_time_frames_combiner(keyword,begin_date='2004-01-01',end_date=date.today())





print(multiple_time_frames_combiner(['Pizza']))




