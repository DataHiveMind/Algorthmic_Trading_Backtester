# src/data_loader.py
import yfinance as yf
import os

def download_data(symbol, start_date, end_date, data_dir='data'):
    """
    Downloads historical stock data from Yahoo Finance and saves it to a CSV file.

    Args:
        symbol (str): The stock ticker symbol (e.g., 'AAPL').
        start_date (str): The start date in 'YYYY-MM-DD' format.
        end_date (str): The end date in 'YYYY-MM-DD' format.
        data_dir (str): The directory to save the data.
    """
    try:
        data = yf.download(symbol, start=start_date, end=end_date)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        filepath = os.path.join(data_dir, f'{symbol}.csv')
        data.to_csv(filepath)
        print(f"Successfully downloaded data for {symbol} and saved to {filepath}")
    except Exception as e:
        print(f"Error downloading data for {symbol}: {e}")

if __name__ == '__main__':
    # Example usage:
    symbol = 'AAPL'
    start = '2020-01-01'
    end = '2023-12-31'
    download_data(symbol, start, end)

    symbol = 'SPY'  # Example ETF
    download_data(symbol, start, end)