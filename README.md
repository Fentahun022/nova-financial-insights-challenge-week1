

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



## Key Project Tasks

*   **Task 1: GitHub & Exploratory Data Analysis (EDA)**
    *   Setting up the Python environment and Git version control.
    *   Performing EDA on news data: descriptive statistics, textual analysis, time series analysis of publication trends, and publisher analysis.
*   **Task 2: Quantitative Analysis using yfinance and TA-Lib**
    *   Loading and preparing historical stock price data.
    *   Calculating technical indicators (Moving Averages, RSI, MACD).
    *   Visualizing stock prices and indicators.
*  **Task 3 :Sentiment Analysis & Correlation (Task 3): publication timestamps.
         Loading historical stock price data from individual CSV files.


## Technologies Used

*   **Programming Language:** Python 3.x
*   **Core Data Science Libraries:** Pandas, NumPy, Matplotlib, Seaborn
*   **Financial Data & Analysis:** `yfinance`, 
*   **Natural Language Processing (NLP):** NLTK, TextBlob
*   **Version Control:**  GitHub
*   **Development Environment:** Jupyter Notebooks, VS Code



