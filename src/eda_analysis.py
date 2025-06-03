
import pandas as pd
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt
import seaborn as sns

def get_descriptive_stats_text(df: pd.DataFrame, text_col_length: str = 'headline_length'):
    """Prints descriptive statistics for text lengths."""
    if text_col_length in df.columns:
        print(f"\n--- Descriptive Statistics for {text_col_length} ---")
        print(df[text_col_length].describe())
        plt.figure(figsize=(10, 5))
        sns.histplot(df[text_col_length], kde=True, bins=30)
        plt.title(f'Distribution of {text_col_length}')
        plt.xlabel('Length (characters)')
        plt.ylabel('Frequency')
        plt.show()
    else:
        print(f"Column '{text_col_length}' not found for descriptive stats.")


def analyze_publishers(df: pd.DataFrame, publisher_col: str = 'publisher', top_n: int = 15):
    """Analyzes and plots publisher activity."""
    if publisher_col in df.columns:
        print(f"\n--- Publisher Analysis (Top {top_n}) ---")
        publisher_counts = df[publisher_col].value_counts().nlargest(top_n)
        print(publisher_counts)
        plt.figure(figsize=(12, 6))
        sns.barplot(x=publisher_counts.index, y=publisher_counts.values)
        plt.title(f'Top {top_n} Most Active Publishers')
        plt.xlabel('Publisher')
        plt.ylabel('Number of Articles')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
    else:
        print(f"Column '{publisher_col}' not found for publisher analysis.")


def analyze_publication_trends(df: pd.DataFrame, date_only_col: str = 'publication_date_only', 
                               day_of_week_col: str = 'publication_day_of_week', 
                               hour_col: str = 'publication_hour'):
    """Analyzes and plots publication trends over time."""
    if date_only_col in df.columns:
        articles_per_day = df.groupby(date_only_col).size()
        plt.figure(figsize=(14, 6))
        articles_per_day.plot(kind='line', marker='.')
        plt.title('Number of Articles Published Over Time')
        plt.xlabel('Date')
        plt.ylabel('Number of Articles')
        plt.grid(True)
        plt.show()

    if day_of_week_col in df.columns:
        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        articles_by_dow = df[day_of_week_col].value_counts().reindex(day_order).fillna(0)
        plt.figure(figsize=(10, 5))
        sns.barplot(x=articles_by_dow.index, y=articles_by_dow.values)
        plt.title('Number of Articles by Day of the Week')
        plt.xlabel('Day of the Week')
        plt.ylabel('Number of Articles')
        plt.show()

    if hour_col in df.columns:
        articles_by_hour = df[hour_col].value_counts().sort_index()
        plt.figure(figsize=(12, 5))
        sns.barplot(x=articles_by_hour.index, y=articles_by_hour.values, color='skyblue')
        plt.title('Number of Articles by Hour of Day (Publisher Timezone)')
        plt.xlabel('Hour of Day')
        plt.ylabel('Number of Articles')
        plt.xticks(range(0,24))
        plt.show()


def extract_common_keywords(df: pd.DataFrame, processed_text_col: str = 'processed_headline', top_n: int = 20):
    """Extracts and plots common keywords (n-grams)."""
    if processed_text_col not in df.columns or df[processed_text_col].isnull().all():
        print(f"Processed text column '{processed_text_col}' not found or empty.")
        return

    # Unigrams
    all_words = " ".join(df[processed_text_col].dropna()).split()
    common_words = Counter(all_words).most_common(top_n)
    df_common_words = pd.DataFrame(common_words, columns=['word', 'count'])
    
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df_common_words, x='count', y='word', palette='viridis')
    plt.title(f'Top {top_n} Most Common Words')
    plt.xlabel('Frequency')
    plt.ylabel('Word')
    plt.show()
    try:
        vectorizer = CountVectorizer(ngram_range=(2, 2), max_features=top_n)
        bigram_matrix = vectorizer.fit_transform(df[processed_text_col].dropna())
        bigram_counts = bigram_matrix.sum(axis=0)
        bigrams_freq = [(word, bigram_counts[0, idx]) for word, idx in vectorizer.vocabulary_.items()]
        bigrams_freq = sorted(bigrams_freq, key = lambda x: x[1], reverse=True)
        df_bigrams = pd.DataFrame(bigrams_freq, columns=['bigram', 'count'])

        plt.figure(figsize=(12, 6))
        sns.barplot(data=df_bigrams, x='count', y='bigram', palette='mako')
        plt.title(f'Top {top_n} Most Common Bigrams')
        plt.xlabel('Frequency')
        plt.ylabel('Bigram')
        plt.show()
    except ValueError as e:
        print(f"Could not generate bigrams: {e}")