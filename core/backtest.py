import numpy as np

def backtest_strategy(
    df,
    cost=0.001,
    conf_threshold=0.52,
    max_drawdown_limit=0.30
):
    """
    Advanced backtesting engine with:
    - Volatility-based position sizing
    - Confidence-weighted exposure
    - Long / Short trading
    - Transaction costs
    - Drawdown-based capital protection
    """

    df = df.copy()

    # ===============================
    # Safety cleanup
    # ===============================
    df = df.dropna(subset=["return", "volatility", "prediction", "confidence"])

    # ===============================
    # Volatility-based base position
    # ===============================
    df["vol_adj"] = df["volatility"].replace(0, np.nan)
    df["base_position"] = 1 / df["vol_adj"]
    df["base_position"] = df["base_position"].clip(upper=3)
    df["base_position"] = df["base_position"].fillna(0)

    # ===============================
    # Confidence weighting
    # ===============================
    df["conf_weight"] = (df["confidence"] - conf_threshold) / (1 - conf_threshold)
    df["conf_weight"] = df["conf_weight"].clip(0, 1)

    # Final position size
    df["position_size"] = df["base_position"] * df["conf_weight"]

    # ===============================
    # Strategy returns (before risk stop)
    # ===============================
    df["strategy_return"] = 0.0

    # Long trades
    df.loc[df["prediction"] == 1, "strategy_return"] = (
        df["return"] * df["position_size"]
    )

    # Short trades
    df.loc[df["prediction"] == 0, "strategy_return"] = (
        -df["return"] * df["position_size"]
    )

    # Transaction cost proportional to exposure
    df["strategy_return"] -= cost * df["position_size"]

    # ===============================
    # Cumulative returns
    # ===============================
    df["cum_strategy"] = (1 + df["strategy_return"]).cumprod()
    df["cum_market"] = (1 + df["return"]).cumprod()

    # ===============================
    # Drawdown calculation
    # ===============================
    df["peak"] = df["cum_strategy"].cummax()
    df["drawdown"] = (df["peak"] - df["cum_strategy"]) / df["peak"]

    # ===============================
    # Drawdown-based stop trading rule
    # ===============================
    stop_idx = df[df["drawdown"] > max_drawdown_limit].index

    if len(stop_idx) > 0:
        first_stop = stop_idx[0]

        # Stop all trading after drawdown breach
        df.loc[first_stop:, "strategy_return"] = 0.0
        df.loc[first_stop:, "position_size"] = 0.0

        # Recompute equity curve correctly
        df["cum_strategy"] = (1 + df["strategy_return"]).cumprod()

    return df
