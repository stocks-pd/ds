from multiprocessing import cpu_count as cpu_count
import requests
import sqlite3
from sqlite3 import Error

# API keys
FMP_KEY_INDEX = 1
FMP_KEY = ['df7afe83903f789adc2f99af26cef1c9',
           "e3b78e56511d7dfdbd8000775c51664c",
           "b0bf65b946c24a87cbd7c605c0bb5239",
           "de5ebe01a82ca44a72f2a2b4d7bc67f4",
           "a2d0ac29f91142e018db0e8a586ff6ad",
           "60ee277f0cde9daa7705f6a79b1f47ba",
           "5b19fce62961a4207f6b574e47f242ba",
           "1a08f439ead54166d7afc86b8149839d",
           "97a0cffc3a6f0bca3301be8ee03bdd08",
           "3ac432c2c30f4b55286659994e6e1112",
           "fd73c0b67949e7f5356c67d219767ab3",
           "85bb050ff332eef4897637accb7c9e04",
           "5812ce3abf6b7718aeb489ffc288f065",
           "c24557db59bf6b80dd54cc86dacbc9ce",
           "9630f8328efd9f2ded97a3592ac6c761",
           "937ea76342f0a99eb456166a11001dc3",
           "3e8cf3f8e72f60540491227b12b07264",
           "942f073828ccda72d278aa608cd3c53e",
           "aaa623a4835fc8826c255ffd1d375e9c",
           "1862c28f578ec3bac1f1f67250d88471",
           "f27c99c0997da9960bded9d03e5b17dc",
           "91c2b5a8d7aecf7c27b92116f98978df",
           "1ebc3f616be306abbee6ea63bbf8d165",
           "709bab142f28fc5c97c1a358a547c0eb",
           "dbe960a0f368d06c49f2748aa5bcd642",
           "6b574ce345b0fe3370403ac4ae9c07b2",
           "9821c9be1c0c2f131a182998a4c5ff68"]
ALPHA_KEY = 'FKJ82GMNFE5Z1Z7Q'
ALPHA_KEY2 = 'ZRMG7N7CVNEFA2RY'

# API queries
# FMP
FMP_TIKER_LABELS = 'https://financialmodelingprep.com/api/v3/financial-statement-symbol-lists?apikey={}'
FMP_STOCK_INFO = 'https://financialmodelingprep.com/api/v3/profile/{}?apikey={}'
FRMP_HISTORICal_DATA = 'https://financialmodelingprep.com/api/v3/historical-price-full/{}?serietype=line&apikey={}'

# Alphavantege
ALPHA_GET_TIKER_HISTORY = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&outputsize=full&apikey={}&datatype=csv'

# Periods of predict
WEEK = 7
MONTH = 31
QUART = MONTH * 3
HALF_YEAR = QUART * 2
YEAR = HALF_YEAR * 2

# Multyproccessing
CPU_COUNT = cpu_count()
PERMISSIBLE_CPU_COUNT = CPU_COUNT - 1

# STOCKS
STOCKS_TIKERS = requests.get(FMP_TIKER_LABELS.format(FMP_KEY[FMP_KEY_INDEX])).json()

# ADDING WORK STOCKS_TICKER IN DATABASE
# sqlite_connection = sqlite3.connect('db.sqlite3')
# cursor = sqlite_connection.cursor()
# print("База данных подключена")
# i = 0
# ERROR_TICKER_COUNT = 0
# for ticker in STOCKS_TIKERS:
#     i+=1
#     if i >250:
#         break
#     CHECK_TICKER= requests.get(FMP_STOCK_INFO.format(ticker,FMP_KEY[FMP_KEY_INDEX])).json()
#     ERROR = "Error Message"
#     FIND_ERROR = ERROR in CHECK_TICKER
#     if (FIND_ERROR):
#         ERROR_TICKER_COUNT+=1
#         print(ERROR_TICKER_COUNT)
#     else:
#
#         cursor.execute("INSERT INTO stock_tickers VALUES  (?)", (ticker,))
#         sqlite_connection.commit()
#         cursor.close



# APIES METHODS
