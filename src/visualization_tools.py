
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_stock_with_indicators(stock_df: pd.DataFrame, ticker: str, 
                               price_col='Close', sma_cols=['SMA_20', 'SMA_50'], 
                               rsi_col='RSI_14', macd_cols=['MACD', 'MACD_signal']):
    """Plots stock price with SMA, RSI, and MACD."""

    plot_df = stock_df.dropna(subset=sma_cols + [rsi_col] + macd_cols).copy()
    if plot_df.empty:
     
        if price_col in stock_df.columns:
            plt.figure(figsize=(14, 7))
            stock_df[price_col].plot(label=f'{ticker} {price_col}')
            plt.title(f'{ticker} {price_col}')
            plt.legend()
            plt.show()
        return

    fig, axes = plt.subplots(3, 1, figsize=(14, 12), sharex=True, 
                             gridspec_kw={'height_ratios': [3, 1, 1]})
    fig.suptitle(f'Technical Indicators for {ticker}', fontsize=16)

    axes[0].plot(plot_df.index, plot_df[price_col], label=f'{ticker} {price_col}', color='blue')
    if sma_cols[0] in plot_df.columns:
        axes[0].plot(plot_df.index, plot_df[sma_cols[0]], label=sma_cols[0], color='orange', alpha=0.7)
    if sma_cols[1] in plot_df.columns:
        axes[0].plot(plot_df.index, plot_df[sma_cols[1]], label=sma_cols[1], color='green', alpha=0.7)
    axes[0].set_ylabel('Price')
    axes[0].legend()
    axes[0].grid(True)


    if rsi_col in plot_df.columns:
        axes[1].plot(plot_df.index, plot_df[rsi_col], label=rsi_col, color='purple')
        axes[1].axhline(70, color='red', linestyle='--', alpha=0.5, label='Overbought (70)')
        axes[1].axhline(30, color='green', linestyle='--', alpha=0.5, label='Oversold (30)')
        axes[1].set_ylabel('RSI')
        axes[1].legend()
        axes[1].grid(True)

    
    if macd_cols[0] in plot_df.columns and macd_cols[1] in plot_df.columns:
        axes[2].plot(plot_df.index, plot_df[macd_cols[0]], label=macd_cols[0], color='red')
        axes[2].plot(plot_df.index, plot_df[macd_cols[1]], label=macd_cols[1], color='cyan')
        if 'MACD_hist' in plot_df.columns: 
             axes[2].bar(plot_df.index, plot_df['MACD_hist'], label='MACD Hist', color='grey', alpha=0.5, width=0.7)
        axes[2].set_ylabel('MACD')
        axes[2].legend()
        axes[2].grid(True)
    
    plt.xlabel('Date')
    plt.tight_layout(rect=[0, 0, 1, 0.96]) 
    plt.show()



def plot_correlation_scatter(df: pd.DataFrame, x_col: str, y_col: str, title: str, stock_symbol:str =""):
    """Plots a scatter plot for correlation analysis."""
    if df is None or df.empty or x_col not in df.columns or y_col not in df.columns:
        print(f"Cannot plot correlation for {stock_symbol}: DataFrame is empty or columns missing.")
        return
    
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x=x_col, y=y_col, alpha=0.5)
   
    if df[[x_col, y_col]].dropna().shape[0] >= 2: 
        correlation = df[x_col].corr(df[y_col])
        plot_title = f'{title} for {stock_symbol}\nCorrelation: {correlation:.2f}'
    else:
        plot_title = f'{title} for {stock_symbol}\nCorrelation: N/A (insufficient data)'
    
    plt.title(plot_title)
    plt.xlabel(x_col.replace('_', ' ').title())
    plt.ylabel(y_col.replace('_', ' ').title())
    plt.grid(True)
    plt.axhline(0, color='grey', linestyle='--')
    plt.axvline(0, color='grey', linestyle='--')
    plt.tight_layout()
    plt.show()
    
if __name__ == '__main__':
     corr_data = pd.DataFrame({
         'avg_sentiment_compound': [0.1, -0.2, 0.5, 0.0, -0.5, 0.8, -0.1, 0.3, 0.2, -0.3],
         'daily_return': [0.01, -0.005, 0.02, 0.001, -0.015, 0.03, 0.00, 0.005, 0.003, -0.008]
     })
     plot_correlation_scatter(corr_data, 'avg_sentiment_compound', 'daily_return', "Sample Sentiment vs. Return", "TEST")