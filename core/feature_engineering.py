import pandas as pd
import numpy as np

def create_features(df, sentiment_score):
    df = df.copy()

    # Price Return
    df["return"] = df["close"].pct_change()

    # Volatility
    df["volatility"] = (
        df["return"]
        .rolling(window=5)
        .std()
    )

    # Sentiment
    df["sentiment"] = sentiment_score

    # Moving Averages
    df["ma5"] = df["close"].rolling(5).mean()
    df["ma10"] = df["close"].rolling(10).mean()
    df["ma20"] = df["close"].rolling(20).mean()

    # Momentum
    df["momentum"] = (
        df["close"] / df["close"].shift(5)
    ) - 1

    # Volume Change
    if "volume" in df.columns:
        df["volume_change"] = (
            df["volume"].pct_change()
        )
    else:
        df["volume_change"] = 0

    # MA Ratio
    df["ma_ratio"] = (
        df["ma5"] / df["ma10"]
    )

    # Distance from MA5
    df["price_vs_ma5"] = (
        df["close"] / df["ma5"]
    ) - 1

    # RSI (14)
    delta = df["close"].diff()

    gain = delta.where(
        delta > 0,
        0
    )

    loss = -delta.where(
        delta < 0,
        0
    )

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss

    df["rsi"] = (
        100 - (100 / (1 + rs))
    )

    # Target
    df["target"] = (
        df["close"]
        .shift(-1)
        > df["close"]
    ).astype(int)

    df = df.dropna()

    return df
