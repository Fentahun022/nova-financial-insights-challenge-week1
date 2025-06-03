
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Project root


DATA_DIR = os.path.join(BASE_DIR, 'data')
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
NEWS_DATA_FILE_PATH = os.path.join(DATA_DIR, 'raw_analyst_ratings.csv') # Example path
NEWS_HEADLINE_COLUMN = 'headline'
NEWS_DATE_COLUMN = 'date'
NEWS_STOCK_COLUMN = 'stock'


STOCK_CSV_DIR_PATH = os.path.join(RAW_DATA_DIR, 'stock_historical_data')
STOCK_FILENAME_TEMPLATE = "{}_historical_data.csv"
STOCK_DATE_COLUMN = 'Date'
STOCK_PRICE_COLUMN_FOR_RETURNS = 'Close' # or 'Adj Close'
STOCK_REQUIRED_OHLCV_COLUMNS = ['Open', 'High', 'Low', 'Close', 'Volume']

SENTIMENT_SCORE_COLUMN = 'sentiment_score' # Output of sentiment analysis


AGG_SENTIMENT_DATE_COLUMN = 'date_sentiment' 
AGG_SENTIMENT_STOCK_COLUMN = 'stock_symbol' 
AGG_SENTIMENT_AVG_SCORE_COLUMN = 'avg_sentiment_score'
AGG_SENTIMENT_NUM_ARTICLES_COLUMN = 'num_articles'

STOCK_DAILY_RETURN_COLUMN = 'daily_return'

MERGED_STOCK_SYMBOL_COLUMN = 'stock_symbol' # Should match AGG_SENTIMENT_STOCK_COLUMN
MERGED_SENTIMENT_SCORE_COLUMN = AGG_SENTIMENT_AVG_SCORE_COLUMN
MERGED_RETURN_COLUMN = STOCK_DAILY_RETURN_COLUMN
MERGED_SENTIMENT_DATE_COLUMN = AGG_SENTIMENT_DATE_COLUMN
MERGED_RETURN_DATE_COLUMN = 'date_return' # Date associated with the return


CORRELATION_LAGS_TO_TEST = [0, 1, -1] # 0:same-day, 1:news->ret_next_day, -1:news->ret_prev_day
CORRELATION_MIN_OBSERVATIONS = 15