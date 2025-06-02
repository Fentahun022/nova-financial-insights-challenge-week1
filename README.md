
*(Note: The `data/` and `reports/` directories are typically not committed if they contain large files or generated artifacts; they are shown here for structural completeness.)*

## Setup and Installation

Follow these steps to set up the project environment:

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/Fentahun022/nova-financial-insights-challenge-week1.git
    cd nova-financial-insights-challenge-week1
    ```

2.  **Create and Activate a Virtual Environment:**
    It's highly recommended to use a virtual environment to manage project dependencies.
    ```bash
    # For Unix/macOS
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    Install all required Python packages listed in `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```
    *   **TA-Lib Note:** The `TA-Lib` library requires pre-installation of its underlying C library. Please refer to the official [TA-Lib Python wrapper documentation](https://mrjbq7.github.io/ta-lib/install.html) for OS-specific installation instructions if you encounter issues. Common steps include:
        *   **Linux (Ubuntu/Debian):** `sudo apt-get install libta-lib-dev`
        *   **macOS:** `brew install ta-lib`
        *   **Windows:** Download precompiled binaries (see documentation).

4.  **Download NLTK Resources (if running text analysis for the first time):**
    Some NLP tasks require NLTK data. This is often handled within the notebooks/scripts, but you might run this once in a Python interpreter within your activated environment:
    ```python
    import nltk
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('vader_lexicon') 
    ```

## Dataset

The primary dataset for this project is the **FNSPID (Financial News and Stock Price Integration Dataset)**. It includes:
*   `headline`: News article headline.
*   `url`: Link to the full article.
*   `publisher`: Publisher of the article.
*   `date`: Publication date and time (UTC-4).
*   `stock`: Associated stock ticker symbol.

Historical stock price data (OHLCV) is fetched using the `yfinance` library.

## How to Run the Analysis

The analysis is primarily conducted through Jupyter Notebooks located in the `notebooks/` directory. It's recommended to run them in the following order:

1.  **`notebooks/01_EDA_News_Data.ipynb`**: Performs Exploratory Data Analysis on the FNSPID dataset, including data cleaning, feature engineering, and visualization of news characteristics.
2.  **`notebooks/02_Quantitative_Stock_Analysis.ipynb`**: Fetches historical stock price data using `yfinance`, calculates various technical indicators (SMA, EMA, RSI, MACD) using `TA-Lib`, and visualizes them. Processed stock data is saved to `data/all_stock_data_with_indicators.pkl`.


## Key Project Tasks

*   **Task 1: GitHub & Exploratory Data Analysis (EDA)**
    *   Setting up the Python environment and Git version control.
    *   Performing EDA on news data: descriptive statistics, textual analysis, time series analysis of publication trends, and publisher analysis.
*   **Task 2: Quantitative Analysis using yfinance and TA-Lib**
    *   Loading and preparing historical stock price data.
    *   Calculating technical indicators (Moving Averages, RSI, MACD).
    *   Visualizing stock prices and indicators.


## Technologies Used

*   **Programming Language:** Python 3.x
*   **Core Data Science Libraries:** Pandas, NumPy, Matplotlib, Seaborn
*   **Financial Data & Analysis:** `yfinance`, `TA-Lib`
*   **Natural Language Processing (NLP):** NLTK, TextBlob/VADER (for sentiment analysis)
*   **Version Control:**  GitHub
*   **Development Environment:** Jupyter Notebooks, VS Code



