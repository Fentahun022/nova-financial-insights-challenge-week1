# src/financial_analysis.py
import pandas as pd
import talib # Make sure TA-Lib C library and Python wrapper are installed
import os
from datetime import timedelta # Not used in this version but often useful

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

                # Check for required OHLCV columns and handle 'Adj Close'
                actual_ohlcv_cols_present = {} # To map required names to actual names in df
                missing_essential_cols = False

                for req_col in required_ohlcv_cols:
                    if req_col in df.columns:
                        actual_ohlcv_cols_present[req_col] = req_col
                    elif req_col == 'Close' and 'Adj Close' in df.columns:
                        print(f"Using 'Adj Close' as 'Close' for {ticker_input} from {file_name}")
                        actual_ohlcv_cols_present['Close'] = 'Adj Close' # Map 'Close' to use 'Adj Close'
                    elif req_col in ['Open', 'High', 'Low', 'Close', 'Volume']: # If other essential cols missing
                        print(f"Warning: Essential OHLCV column '{req_col}' missing in {file_name} for {ticker_input}.")
                        missing_essential_cols = True
                        break
                
                if missing_essential_cols:
                    print(f"Skipping {ticker_input} due to missing essential OHLCV columns.")
                    continue

                # Create a new DataFrame with standardized column names if mapping occurred
                processed_df_data = {}
                for req_col in required_ohlcv_cols:
                    if req_col in actual_ohlcv_cols_present:
                         processed_df_data[req_col] = df[actual_ohlcv_cols_present[req_col]]
                    elif req_col not in ['Open', 'High', 'Low', 'Close', 'Volume']: # Non-essential, can be NaN
                        processed_df_data[req_col] = pd.Series(index=df.index, dtype=float) # Empty series of NaN


                processed_df = pd.DataFrame(processed_df_data, index=df.index)

                # Ensure numeric and drop rows with NaNs in essential OHLCV columns
                cols_to_numerify = [col for col in ['Open', 'High', 'Low', 'Close', 'Volume'] if col in processed_df.columns]
                for col in cols_to_numerify:
                    processed_df[col] = pd.to_numeric(processed_df[col], errors='coerce')
                
                processed_df.dropna(subset=cols_to_numerify, inplace=True)

                if processed_df.empty:
                    print(f"Warning: No valid data remaining in {file_name} for {ticker_input} after processing. Skipping.")
                    continue
                    
                stock_data_dict[ticker_case_for_file] = processed_df # Store with consistent uppercase ticker key
            except Exception as e:
                print(f"Error loading or processing {file_name} for ticker {ticker_input}: {e}")
        else:
            # This warning is normal if you don't have CSVs for all tickers from news
            # print(f"Info: Stock CSV file not found for ticker {ticker_case_for_file} at {file_path}")
            pass # Suppress for cleaner output unless debugging specific file loading

    if not stock_data_dict:
        print("No stock data successfully loaded from any CSV files.")
    return stock_data_dict

def calculate_technical_indicators(stock_df: pd.DataFrame, price_col: str = 'Close') -> pd.DataFrame:
    """Calculates SMA, RSI, MACD for a stock DataFrame. Ensures columns are created even if all NaN."""
    df = stock_df.copy()

    # Initialize TA columns with pd.NA to ensure they exist
    ta_columns = ['SMA_20', 'SMA_50', 'RSI_14', 'MACD', 'MACD_signal', 'MACD_hist']
    for col in ta_columns:
        if col not in df.columns: # Check if column already exists (e.g. from partial processing)
            df[col] = pd.NA # Use pandas NA for missing indicator values

    if price_col not in df.columns or df[price_col].isnull().all():
        print(f"Price column '{price_col}' (for TA) not found or is all NaN in DataFrame for ticker. Skipping TA calculation, columns will remain NA.")
        return df

    df[price_col] = pd.to_numeric(df[price_col], errors='coerce')
    if df[price_col].isnull().all():
        print(f"Price column '{price_col}' became all NaN after numeric conversion. Skipping TA, columns will remain NA.")
        return df
    
    # Define minimum periods required for each TA-Lib function
    # These are approximate; TA-Lib handles exacts but good for conditional calculation
    min_len_sma20 = 20
    min_len_sma50 = 50
    min_len_rsi = 14 + 1  # RSI usually needs N periods + 1 for first calculation
    min_len_macd_slow = 26 # Based on slow period of MACD
    min_len_macd_signal = min_len_macd_slow + 9 # Approx for signal line

    # Calculate SMAs
    if len(df[price_col].dropna()) >= min_len_sma20:
        df['SMA_20'] = talib.SMA(df[price_col], timeperiod=20)
    else:
        # print(f"Warning: Data for TA too short for SMA_20 (valid data points {len(df[price_col].dropna())} < {min_len_sma20})")
        pass # Column already initialized with pd.NA

    if len(df[price_col].dropna()) >= min_len_sma50:
        df['SMA_50'] = talib.SMA(df[price_col], timeperiod=50)
    else:
        # print(f"Warning: Data for TA too short for SMA_50 (valid data points {len(df[price_col].dropna())} < {min_len_sma50})")
        pass

    # Calculate RSI
    if len(df[price_col].dropna()) >= min_len_rsi:
        df['RSI_14'] = talib.RSI(df[price_col], timeperiod=14)
    else:
        # print(f"Warning: Data for TA too short for RSI_14 (valid data points {len(df[price_col].dropna())} < {min_len_rsi})")
        pass
    
    # Calculate MACD
    # MACD requires enough data for its slowest EMA (26 periods) + signal line (9 periods) to be meaningful
    # TA-Lib's MACD function returns NaNs if data is too short.
    if len(df[price_col].dropna()) >= min_len_macd_signal : # Check against a more comprehensive length
        try:
            macd, macdsignal, macdhist = talib.MACD(df[price_col], fastperiod=12, slowperiod=26, signalperiod=9)
            df['MACD'] = macd
            df['MACD_signal'] = macdsignal
            df['MACD_hist'] = macdhist
        except Exception as e:
            print(f"Error calculating MACD with TA-Lib (data length {len(df[price_col].dropna())}): {e}. Columns remain NA.")
            # Columns MACD, MACD_signal, MACD_hist are already pd.NA
    else:
        # print(f"Warning: Data for TA too short for full MACD calculation (valid data points {len(df[price_col].dropna())} < {min_len_macd_signal} approx)")
        pass # Columns already pd.NA
            
    return df