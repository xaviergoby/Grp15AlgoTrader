import pandas as pd



def SMA(data, trend_period_days=21):
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


def RSI(dataframe, column="Close", period=14):
    """
    Relative Strength Index
    """

    delta = dataframe[column].diff()
    up, down = delta.copy(), delta.copy()

    up[up < 0] = 0
    down[down > 0] = 0

    roll_up = up.ewm(com=period - 1, adjust=False).mean()
    roll_down = down.ewm(com=period - 1, adjust=False).mean().abs()

    rsi = 100 - 100 / (1 + roll_up / roll_down)

    return dataframe.join(rsi.to_frame('RSI'))


def EMA(data, trend_period_days=21, return_data = False):
    """
    Exponential Moving Average
    """
    trend_period_name = str(trend_period_days) + "d"
    dt_dates_list = data.index.date.tolist()
    close = data.Close
    trend = data.Close.ewm(span=trend_period_days).mean()
    ema_trend = pd.DataFrame({"Dates":dt_dates_list, "Close":close.values, trend_period_name:trend.values}, index=range(len(dt_dates_list)))
    
    if return_data is False:     
        return ema_trend
    else:
        return trend


def MACD(data, ema_days_upper=26, ema_days_lower=12):
    """
    Moving Average Convergence Divergence
    """
    dt_dates_list = data.index.date.tolist()
    close = data.Close
    
    ema_trend_26d = EMA(data, trend_period_days=ema_days_upper, return_data=True)
    ema_trend_12d = EMA(data, trend_period_days=ema_days_lower, return_data=True)
    trend = ema_trend_26d - ema_trend_12d
    macd_trend = pd.DataFrame({"Dates":dt_dates_list, "Close":close.values, "MACD":trend.values })
    
    return macd_trend
