
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Ensure NLTK resources are available
try:
    stopwords.words('english')
    word_tokenize("test")
except LookupError:
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)

def load_financial_news_data(file_path: str) -> pd.DataFrame:
    """Loads the financial news dataset."""
    try:
        df = pd.read_csv(file_path)
      
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df.dropna(subset=['date'], inplace=True) 
        return df
    except FileNotFoundError:
        print(f"Error: Dataset file not found at {file_path}.")
       
        dummy_data = {
            'headline': ["Stock Alpha Soars", "Beta Corp Earnings Miss", "Gamma Inc Price Target Up"],
            'url': ["url1", "url2", "url3"],
            'publisher': ["NewsHub", "FinanceTimes", "NewsHub"],
            'date': [pd.Timestamp("2023-01-15 09:30:00-04:00", tz='America/New_York'), 
                     pd.Timestamp("2023-01-15 10:00:00-04:00", tz='America/New_York'),
                     pd.Timestamp("2023-01-16 14:00:00-04:00", tz='America/New_York')],
            'stock': ["ALPHA", "BETA", "GAMMA"]
        }
        df = pd.DataFrame(dummy_data)
        df['date'] = pd.to_datetime(df['date'])
        return df


def preprocess_text_data(df: pd.DataFrame, text_col: str = 'headline') -> pd.DataFrame:
    """Adds processed text columns for EDA and NLP."""
    df_copy = df.copy()
    if text_col not in df_copy.columns:
        print(f"Warning: Column '{text_col}' not found for preprocessing.")
        return df_copy

    df_copy['headline_length'] = df_copy[text_col].astype(str).str.len()
    
 
    stop_words_set = set(stopwords.words('english'))
    
    def clean_text(text):
        if not isinstance(text, str): return ""
        text = text.lower()
        text = re.sub(r'\W+', ' ', text)
        tokens = word_tokenize(text)
        # Keep words with > 2 chars, not in stopwords
        tokens = [word for word in tokens if len(word) > 2 and word not in stop_words_set]
        return " ".join(tokens)

    df_copy[f'processed_{text_col}'] = df_copy[text_col].apply(clean_text)
    return df_copy

def extract_date_features(df: pd.DataFrame, date_col: str = 'date') -> pd.DataFrame:
    """Extracts date-based features for time series analysis."""
    df_copy = df.copy()
    if date_col not in df_copy.columns or df_copy[date_col].isnull().all():
        print(f"Warning: Date column '{date_col}' not found or is all NaT.")
        return df_copy
    
    df_copy['publication_date_only'] = df_copy[date_col].dt.date
    df_copy['publication_year'] = df_copy[date_col].dt.year
    df_copy['publication_month'] = df_copy[date_col].dt.month
    df_copy['publication_day_of_week'] = df_copy[date_col].dt.day_name()
    df_copy['publication_hour'] = df_copy[date_col].dt.hour
    return df_copy