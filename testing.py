from technical_indicators.simple_moving_avg import *
from data_loader.data_sources import *

data = get_stocks_data()
data_with_rsi = MACD(data)
print(data_with_rsi)
