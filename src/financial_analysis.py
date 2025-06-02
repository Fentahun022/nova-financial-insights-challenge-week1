
import pandas as pd
import os

def load_stock_prices_from_csvs(tickers: list,
                                csv_directory: str,
                                filename_template: str = "{}_historical_data.csv",
                                date_col: str = 'Date',
                                required_ohlcv_cols: list = None) -> dict:
    """
    Loads OHLCV data for given tickers from local CSV files.
    Tickers in the input list are uppercased to match common filename conventions.
    """
    stock_data_dict = {}
    if required_ohlcv_cols is None:
        required_ohlcv_cols = ['Open', 'High', 'Low', 'Close', 'Volume']

    print(f"Attempting to load stock data from CSVs in directory: {csv_directory}")
    print(f"Using filename template: {filename_template} and date column: {date_col}")

    for ticker_input in tickers:
        ticker_case_for_file = str(ticker_input).upper() # Ensure string and uppercase

        file_name = filename_template.format(ticker_case_for_file)
        file_path = os.path.join(csv_directory, file_name)

        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path)
                
                if date_col not in df.columns:
                    print(f"Warning: Date column '{date_col}' not found in {file_name} for ticker {ticker_input}. Skipping.")
                    continue
                
                df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
                df.dropna(subset=[date_col], inplace=True)
                if df.empty:
                    print(f"Warning: No valid dates in {file_name} for ticker {ticker_input} after conversion. Skipping.")
                    continue
                df.set_index(date_col, inplace=True)
                df.sort_index(inplace=True)

                actual_ohlcv_cols_present = {}
                missing_essential_cols = False

                for req_col in required_ohlcv_cols:
                    if req_col in df.columns:
                        actual_ohlcv_cols_present[req_col] = req_col
                    elif req_col.lower() in df.columns.str.lower().values: # Case-insensitive check
                        actual_col_name = df.columns[df.columns.str.lower() == req_col.lower()][0]
                        actual_ohlcv_cols_present[req_col] = actual_col_name
                        print(f"Found '{actual_col_name}' for required '{req_col}' in {ticker_input}.")
                    elif req_col == 'Close' and 'Adj Close' in df.columns:
                        actual_ohlcv_cols_present['Close'] = 'Adj Close'
                    elif req_col == 'Close' and df.columns.str.lower().isin(['adj close', 'adjusted close']).any():
                        adj_close_col = df.columns[df.columns.str.lower().isin(['adj close', 'adjusted close'])][0]
                        actual_ohlcv_cols_present['Close'] = adj_close_col
                        print(f"Using '{adj_close_col}' as 'Close' for {ticker_input} from {file_name}")
                    elif req_col in ['Open', 'High', 'Low', 'Close', 'Volume']:
                        print(f"Warning: Essential OHLCV column '{req_col}' missing in {file_name} for {ticker_input}.")
                        missing_essential_cols = True
                        break
                
                if missing_essential_cols:
                    print(f"Skipping {ticker_input} due to missing essential OHLCV columns.")
                    continue

                processed_df_data = {}
                for req_col in required_ohlcv_cols:
                    if req_col in actual_ohlcv_cols_present:
                         processed_df_data[req_col] = df[actual_ohlcv_cols_present[req_col]]
                    # If a non-essential column (not in Open, High, Low, Close, Volume) is missing, it's okay
                    elif req_col not in ['Open', 'High', 'Low', 'Close', 'Volume']:
                        # It will just not be in processed_df_data, pandas handles missing columns fine
                        pass

                processed_df = pd.DataFrame(processed_df_data, index=df.index)
                
                # Standardize column names to 'Open', 'High', 'Low', 'Close', 'Volume'
                rename_map = {}
                for req_col in required_ohlcv_cols:
                    if req_col in actual_ohlcv_cols_present and actual_ohlcv_cols_present[req_col] != req_col:
                        rename_map[actual_ohlcv_cols_present[req_col]] = req_col
                
                # The processed_df should already have the correct target names
                # from the processed_df_data dictionary keys.

                cols_to_numerify = [col for col in ['Open', 'High', 'Low', 'Close', 'Volume'] if col in processed_df.columns]
                for col in cols_to_numerify:
                    processed_df[col] = pd.to_numeric(processed_df[col], errors='coerce')
                
                processed_df.dropna(subset=cols_to_numerify, inplace=True)

                if processed_df.empty:
                    print(f"Warning: No valid data remaining in {file_name} for {ticker_input} after processing. Skipping.")
                    continue
                    
                stock_data_dict[ticker_case_for_file] = processed_df
            except Exception as e:
                print(f"Error loading or processing {file_name} for ticker {ticker_input}: {e}")
        else:
            # print(f"Info: Stock CSV file not found for ticker {ticker_case_for_file} at {file_path}")
            pass

    if not stock_data_dict:
        print("No stock data successfully loaded from any CSV files.")
    return stock_data_dict

def calculate_technical_indicators(stock_df: pd.DataFrame, price_col: str = 'Close') -> pd.DataFrame:
    """
    Calculates SMA, RSI, MACD for a stock DataFrame using pandas.
    Ensures columns are created even if results are all NaN.
    """
    df = stock_df.copy()

    # Initialize TA columns with pd.NA to ensure they exist
    ta_columns = ['SMA_20', 'SMA_50', 'RSI_14', 'MACD', 'MACD_signal', 'MACD_hist']
    for col in ta_columns:
        if col not in df.columns:
            df[col] = pd.NA # Use pandas NA for missing indicator values

    if price_col not in df.columns or df[price_col].isnull().all():
        print(f"Price column '{price_col}' (for TA) not found or is all NaN. Skipping TA calculation, columns will remain NA.")
        return df

    # Ensure price column is numeric
    prices = pd.to_numeric(df[price_col], errors='coerce')
    if prices.isnull().all():
        print(f"Price column '{price_col}' became all NaN after numeric conversion. Skipping TA, columns will remain NA.")
        return df

    # SMA (Simple Moving Average)
    sma_20_period = 20
    sma_50_period = 50
    if len(prices.dropna()) >= sma_20_period:
        df['SMA_20'] = prices.rolling(window=sma_20_period, min_periods=sma_20_period).mean()
    if len(prices.dropna()) >= sma_50_period:
        df['SMA_50'] = prices.rolling(window=sma_50_period, min_periods=sma_50_period).mean()

    # RSI (Relative Strength Index)
    rsi_period = 14
    if len(prices.dropna()) >= rsi_period + 1: # RSI needs at least period+1 to calculate first diff
        delta = prices.diff()
        
        gain = delta.where(delta > 0, 0.0) # Ensure float for ewm
        loss = -delta.where(delta < 0, 0.0) # Ensure float for ewm

        # Use com for smoothing factor alpha=1/N, similar to Wilder's MA used in TA-Lib RSI
        # TA-Lib's RSI uses Wilder's smoothing. adjust=False is important for EMA-like behavior.
        avg_gain = gain.ewm(com=rsi_period - 1, min_periods=rsi_period, adjust=False).mean()
        avg_loss = loss.ewm(com=rsi_period - 1, min_periods=rsi_period, adjust=False).mean()
        
        rs = avg_gain / avg_loss
        df['RSI_14'] = 100.0 - (100.0 / (1.0 + rs))
        # Handle cases where avg_loss is 0 (RSI becomes 100)
        df.loc[avg_loss == 0, 'RSI_14'] = 100.0
        # Handle cases where avg_gain and avg_loss are 0 (RSI becomes NaN or 0, often 50 is used as neutral)
        # Pandas ewm will propagate NaNs if not enough data, which is fine.
    
    # MACD (Moving Average Convergence Divergence)
    ema_fast_period = 12
    ema_slow_period = 26
    macd_signal_period = 9

    if len(prices.dropna()) >= ema_slow_period: # Need at least enough for the slowest EMA
        ema_fast = prices.ewm(span=ema_fast_period, adjust=False, min_periods=ema_fast_period).mean()
        ema_slow = prices.ewm(span=ema_slow_period, adjust=False, min_periods=ema_slow_period).mean()
        
        df['MACD'] = ema_fast - ema_slow
        
        if len(df['MACD'].dropna()) >= macd_signal_period:
            df['MACD_signal'] = df['MACD'].ewm(span=macd_signal_period, adjust=False, min_periods=macd_signal_period).mean()
            df['MACD_hist'] = df['MACD'] - df['MACD_signal']
            
    return df