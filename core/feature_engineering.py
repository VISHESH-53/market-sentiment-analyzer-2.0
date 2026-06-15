import pandas as pd

def create_features(price_df, sentiment_score):
    df = price_df.copy()

    df['return'] = df['close'].pct_change()
    df['volatility'] = df['return'].rolling(3).std()
    df['sentiment'] = sentiment_score
    df["ma5"] = df["close"].rolling(5).mean()

    df["ma10"] = df["close"].rolling(10).mean()
    
    df["momentum"] = df["close"] / df["close"].shift(5) - 1
    
    df["volume_change"] = (
        df["volume"] / df["volume"].shift(1) - 1
    )
    
    df["ma_ratio"] = df["ma5"] / df["ma10"]
    
    df["price_vs_ma5"] = (
        df["close"] / df["ma5"] - 1
    )
    # 🎯 TARGET: next-day direction
    df['target'] = (df['return'].shift(-1) > 0).astype(int)

    df = df.dropna()
    return df
