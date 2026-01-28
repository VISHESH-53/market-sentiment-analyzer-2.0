import numpy as np

def backtest_strategy(
    df,
    cost=0.001,
    conf_threshold=0.52,
    max_drawdown_limit=0.30
):
    """
    Backtest with:
    - volatility-based position sizing
    - confidence-weighted exposure
    - transaction costs
    - drawdown-based stop trading rule
    """

    df = df.copy()
    df = df.dropna(subset=["return", "volatility", "prediction", "confidence"])

    # ===============================
    # Volatility-based base position
    # ===============================
    df["vol_adj"] = df["volatility"].replace(0, np.nan)
    df["base_position"] = 1 / df["vol_adj"]
    df["base_position"] = df["base_position"].clip(upper=3)

    # ===============================
    # Confidence weighting (row-wise)
    # ===============================
    df["conf_weight"] = (df["confidence"] - conf_threshold) / (1 - conf_threshold)
    df["conf_weight"] = df["conf_weight"].clip(lower=0, upper=1)

    df["position_size"] = df["base_position"] * df["conf_weight"]
    df["position_size"] = df["position_size"].fillna(0)

    # ===============================
    # Strategy returns (pre-risk-stop)
    # ===============================
    df["strategy_return"] = 0.0

    df.loc[df["prediction"] == 1, "strategy_return"] = (
        df["return"] * df["position_size"]
    )

    df.loc[df["prediction"] == 0, "strategy_return"] = (
        -df["return"] * df["position_size"]
    )

    # Transaction cost
    df.loc[df["position_size"] > 0, "strategy_return"] -= cost

    # ===============================
    # Apply drawdown stop rule
    # ===============================
    df["cum_strategy"] = (1 + df["strategy_return"]).cumprod()
    df["peak"] = df["cum_strategy"].cummax()
    df["drawdown"] = (df["peak"] - df["cum_strategy"]) / df["peak"]

    # Once drawdown exceeds limit → stop trading
    stop_index = df[df["drawdown"] > max_drawdown_limit].index

    if len(stop_index) > 0:
        first_stop = stop_index[0]
        df.loc[first_stop:, "strategy_return"] = 0.0
        df.loc[first_stop:, "position_size"] = 0.0
        df.loc[first_stop:, "cum_strategy"] = df.loc[first_stop, "cum_strategy"]

    # Market benchmark
    df["cum_market"] = (1 + df["return"]).cumprod()

    return df
