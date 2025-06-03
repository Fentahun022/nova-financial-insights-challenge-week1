
import pandas as pd
import numpy as np
from scipy.stats import pearsonr
from . import config 

def aggregate_daily_sentiment(
    news_df_with_sentiment,
    date_col=config.AGG_SENTIMENT_DATE_COLUMN,       
    stock_col=config.NEWS_STOCK_COLUMN,           
    sentiment_col=config.SENTIMENT_SCORE_COLUMN,  
    output_stock_col=config.AGG_SENTIMENT_STOCK_COLUMN,
    output_avg_sentiment_col=config.AGG_SENTIMENT_AVG_SCORE_COLUMN,
    output_num_articles_col=config.AGG_SENTIMENT_NUM_ARTICLES_COLUMN
):
    """Aggregates sentiment scores by stock and date (daily)."""
    if news_df_with_sentiment.empty or not all(c in news_df_with_sentiment.columns for c in [date_col, stock_col, sentiment_col]):
      
        return pd.DataFrame()

    df_agg = news_df_with_sentiment.copy()
    df_agg[stock_col] = df_agg[stock_col].astype(str).str.upper()
    
    if not pd.api.types.is_datetime64_any_dtype(df_agg[date_col]):
        df_agg[date_col] = pd.to_datetime(df_agg[date_col], errors='coerce')
    df_agg.dropna(subset=[date_col], inplace=True)


    aggregated = df_agg.groupby([date_col, stock_col]).agg(
        avg_sentiment=(sentiment_col, 'mean'),
        num_articles=(sentiment_col, 'count') # Count non-NA sentiment scores
    ).reset_index()


    aggregated.rename(columns={
        date_col: config.AGG_SENTIMENT_DATE_COLUMN, 
        stock_col: output_stock_col,
        'avg_sentiment': output_avg_sentiment_col,
        'num_articles': output_num_articles_col
    }, inplace=True)
    
    print(f"Daily sentiment aggregation complete. Result shape: {aggregated.shape}")
    return aggregated

def calculate_daily_stock_returns(
    stock_df: pd.DataFrame,
    price_col=config.STOCK_PRICE_COLUMN_FOR_RETURNS,
    output_col=config.STOCK_DAILY_RETURN_COLUMN
) -> pd.DataFrame:
    """Calculates daily percentage stock returns."""
    if stock_df is None or stock_df.empty:
      
        return pd.DataFrame(columns=[output_col]) 

    df = stock_df.copy()
    if price_col not in df.columns:
       
        df[output_col] = np.nan
        return df

    if not pd.api.types.is_numeric_dtype(df[price_col]):
        df[price_col] = pd.to_numeric(df[price_col], errors='coerce')
    
    if df[price_col].isnull().all():
       
        df[output_col] = np.nan
    else:
        df[output_col] = df[price_col].pct_change()
    return df

def merge_sentiment_with_returns(
    aggregated_sentiment_df,
    stock_data_with_returns_dict: dict, # Dict of {TICKER: df_with_returns}
    sentiment_stock_col=config.AGG_SENTIMENT_STOCK_COLUMN,
    sentiment_date_col=config.AGG_SENTIMENT_DATE_COLUMN,
    sentiment_score_col=config.AGG_SENTIMENT_AVG_SCORE_COLUMN,
    stock_return_col=config.STOCK_DAILY_RETURN_COLUMN,
    lag_days: int = 0,
    output_merged_stock_col=config.MERGED_STOCK_SYMBOL_COLUMN,
    output_merged_sentiment_date_col=config.MERGED_SENTIMENT_DATE_COLUMN,
    output_merged_return_date_col=config.MERGED_RETURN_DATE_COLUMN
):
    """
    Merges aggregated daily sentiment with daily stock returns, applying a lag to returns.
    lag_days > 0: sentiment today vs future return (return shifted backwards)
    lag_days < 0: sentiment today vs past return (return shifted forwards)
    lag_days = 0: contemporary
    """
    if aggregated_sentiment_df.empty or not stock_data_with_returns_dict:
     
        return pd.DataFrame()

    all_merged_data = []

    if not pd.api.types.is_datetime64_any_dtype(aggregated_sentiment_df[sentiment_date_col]):
         aggregated_sentiment_df[sentiment_date_col] = pd.to_datetime(aggregated_sentiment_df[sentiment_date_col], errors='coerce')

    for stock_symbol_key, stock_df in stock_data_with_returns_dict.items():
    
        sentiment_for_stock = aggregated_sentiment_df[
            aggregated_sentiment_df[sentiment_stock_col] == stock_symbol_key
        ].copy()

        if sentiment_for_stock.empty or stock_return_col not in stock_df.columns:
            continue
        
    
        temp_stock_df = stock_df.copy()
        if not isinstance(temp_stock_df.index, pd.DatetimeIndex):
        
            continue
    
        temp_stock_df['shifted_return'] = temp_stock_df[stock_return_col].shift(-lag_days)
        temp_stock_df.rename(columns={sentiment_date_col: output_merged_return_date_col}, inplace=True, errors='ignore') # In case stock_df has a date column
        temp_stock_df.index.name = output_merged_return_date_col 
        sentiment_for_stock.rename(columns={sentiment_date_col: output_merged_sentiment_date_col}, inplace=True)

        merged_stock = pd.merge(
            sentiment_for_stock[[output_merged_sentiment_date_col, sentiment_score_col, config.AGG_SENTIMENT_NUM_ARTICLES_COLUMN]],
            temp_stock_df[['shifted_return']].reset_index(), 
            left_on=output_merged_sentiment_date_col,
            right_on=output_merged_return_date_col,
            how='inner'
        )

        if not merged_stock.empty:
            merged_stock[output_merged_stock_col] = stock_symbol_key 
            merged_stock.rename(columns={'shifted_return': stock_return_col}, inplace=True) 
            all_merged_data.append(merged_stock)

    if not all_merged_data:
      
        return pd.DataFrame()

    final_merged_df = pd.concat(all_merged_data, ignore_index=True)

    return final_merged_df


def calculate_pearson_correlation(
    df,
    col1,
    col2,
    min_observations=config.CORRELATION_MIN_OBSERVATIONS
):
    """Calculates Pearson correlation if enough observations exist."""
    if df.empty or not all(c in df.columns for c in [col1, col2]):
        return np.nan, 0

    temp_df = df[[col1, col2]].dropna()
    n_obs = len(temp_df)

    if n_obs < min_observations:
        return np.nan, n_obs
    
    if len(temp_df[col1].unique()) == 1 or len(temp_df[col2].unique()) == 1: # Avoid constant series error
        return np.nan, n_obs

    correlation = temp_df[col1].corr(temp_df[col2], method='pearson')
    return correlation, n_obs