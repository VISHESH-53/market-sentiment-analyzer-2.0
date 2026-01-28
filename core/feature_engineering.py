import pandas as pd

def create_features(price_df, sentiment_score):
    df = price_df.copy()

    df['return'] = df['close'].pct_change()
    df['volatility'] = df['return'].rolling(3).std()
    df['sentiment'] = sentiment_score

    # 🎯 TARGET: next-day direction
    df['target'] = (df['return'].shift(-1) > 0).astype(int)

    df = df.dropna()
    return df
