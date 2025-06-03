# src/sentiment_tool.py
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def get_sentiment_scores_vader(text):
    if not isinstance(text, str):
        return {'neg': 0.0, 'neu': 1.0, 'pos': 0.0, 'compound': 0.0}
    vs = analyzer.polarity_scores(text)
    return vs

def add_sentiment_to_df(df: pd.DataFrame, text_column: str) -> pd.DataFrame:
    if df is None or text_column not in df.columns:
        print(f"Error: DataFrame is None or text column '{text_column}' not found.")
        return df if df is not None else pd.DataFrame()

    df_copy = df.copy()
    sentiment_scores_list = df_copy[text_column].apply(get_sentiment_scores_vader)
    sentiment_df = pd.json_normalize(sentiment_scores_list)
    sentiment_df.columns = [f'sentiment_{col}' for col in sentiment_df.columns]
    
    df_with_sentiment = pd.concat([df_copy, sentiment_df.set_index(df_copy.index)], axis=1)
    
    def sentiment_label(compound_score):
        if compound_score >= 0.05: return 'positive'
        elif compound_score <= -0.05: return 'negative'
        else: return 'neutral'
            
    df_with_sentiment['sentiment_label'] = df_with_sentiment['sentiment_compound'].apply(sentiment_label)
    print(f"Sentiment scores added to DataFrame using column '{text_column}'.")
    return df_with_sentiment

if __name__ == '__main__':
    sample_data = {'processed_headline': ['good news today', 'bad news yesterday', 'neutral statement']}
    sample_df = pd.DataFrame(sample_data)
    result_df = add_sentiment_to_df(sample_df, 'processed_headline')
    print(result_df)