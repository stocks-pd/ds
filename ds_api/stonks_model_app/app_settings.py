from multiprocessing import cpu_count as cpu_count

# API keys
FMP_KEY = 'df7afe83903f789adc2f99af26cef1c9'
ALPHA_KEY = 'ZRMG7N7CVNEFA2RY'

# API queries
# FMP
FMP_TIKER_LABELS = 'https://financialmodelingprep.com/api/v3/financial-statement-symbol-lists?apikey={}'

# Alphavantege
ALPHA_GET_TIKER_HISTORY = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}' \
                          '&outputsize=full&apikey={}&datatype=csv'

# Periods of predict
WEEK = 7
MONTH = 31
QUART = MONTH * 3
HALF_YEAR = QUART * 2
YEAR = HALF_YEAR * 2

# Multyproccessing
CPU_COUNT = cpu_count()
PERMISSIBLE_CPU_COUNT = CPU_COUNT - 1
