import yfinance as yf
import pandas as pd

def fetch_market_data(symbol, period="1mo"):
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period)

        if df.empty:
            return None

        df = df.reset_index()

        # Normalize column names
        df.columns = [c.lower() for c in df.columns]

        # Rename date column
        if 'date' in df.columns:
            df.rename(columns={'date': 'datetime'}, inplace=True)

        # Keep only required columns
        df = df[['datetime', 'open', 'high', 'low', 'close']]

        # Ensure numeric
        for col in ['open', 'high', 'low', 'close']:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        df = df.dropna()

        return df

    except Exception as e:
        print("Market data error:", e)
        return None
