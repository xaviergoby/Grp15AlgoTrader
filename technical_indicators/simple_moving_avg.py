import pandas as pd



def simple_moving_avg(data, trend_period_days=21):
    """
    The Simple Moving Average (Rolling Window) Indicator
    :param data: The original OHCLV and VWAP pandas DataFrame output of i.e. the data_loader.data_sources.get_stocks_data()
    :param trend_period_days: Int of the time period for computing the trend line values. Is 21 by default
    :return: A pandas DataFrame consisting of the columns ["Date", "Close", "<time period>d"]
    """
    trend_period_name = str(trend_period_days) + "d"
    dt_dates_list = data.index.date.tolist()
    close = data.Close
    trend = data.Close.rolling(window=trend_period_days).mean()
    sma_trend = pd.DataFrame({"Dates":dt_dates_list, "Close":close.values, trend_period_name:trend.values}, index=range(len(dt_dates_list)))
    return sma_trend

