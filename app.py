# ================== PATH & MODULE LOADER ==================
import sys
import os
import importlib.util

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

def load_module(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Load report modules explicitly (Windows-safe)
report_assets = load_module(
    "report_assets",
    os.path.join(PROJECT_ROOT, "core", "report_assets.py")
)

report_generator = load_module(
    "report_generator",
    os.path.join(PROJECT_ROOT, "core", "report_generator.py")
)

# ================== SAFE IMPORTS ==================
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from core.fetch_market_data import fetch_market_data
from core.fetch_news import fetch_news
from core.sentiment import analyze_sentiment, get_sentiment_label
from core.feature_engineering import create_features
from core.trading_signal import generate_signal
from core.backtest import backtest_strategy
from core.risk_metrics import sharpe_ratio, max_drawdown
from core.walk_forward import walk_forward_validation

# ================== STREAMLIT CONFIG ==================
st.set_page_config(page_title="Market Sentiment Analyzer", layout="wide")

st.title("📊 Quantitative Market Sentiment Analyzer 2.0")
st.markdown("Stocks & Crypto | Price + News Sentiment | ML | Backtesting")

# ================== SIDEBAR ==================
st.sidebar.header("🔍 Market Selection")
symbol = st.sidebar.text_input("Enter Stock / Crypto Symbol", value="AAPL")

period = st.sidebar.selectbox(
    "Select Time Period",
    ["5d", "1mo", "3mo", "6mo", "1y"],
    index=4   # default = "1y"
)


# ================== MARKET DATA ==================
data = fetch_market_data(symbol, period)

if data is None:
    st.error("No market data available")
    st.stop()

data = data[data["close"] > 0]

st.subheader(f"📈 Price Chart – {symbol}")

fig = go.Figure(
    data=[
        go.Candlestick(
            x=data["datetime"],
            open=data["open"],
            high=data["high"],
            low=data["low"],
            close=data["close"],
        )
    ]
)

fig.update_layout(
    height=500,
    template="plotly_dark",
    xaxis_title="Date",
    yaxis_title="Price",
    xaxis_rangeslider_visible=False,
)

st.plotly_chart(fig, use_container_width=True)

# ================== NEWS & SENTIMENT ==================
st.subheader("📰 Market News & Sentiment")

avg_sentiment = 0.0
query = symbol.replace("-USD", "")
articles = fetch_news(query)

sentiment_scores = []
for article in articles:
    text = f"{article['title']} {article.get('description', '')}"
    sentiment_scores.append(analyze_sentiment(text))

if sentiment_scores:
    avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)
    label = get_sentiment_label(avg_sentiment)

    col1, col2 = st.columns(2)
    col1.metric("Sentiment Score", round(avg_sentiment, 3))
    col2.metric("Market Mood", label)

    st.markdown("### Sentiment Strength")
    st.progress(min(max((avg_sentiment + 1) / 2, 0), 1))
else:
    st.warning("No news found for sentiment analysis.")

# ================== ML PREDICTION (WALK-FORWARD) ==================
st.subheader("🤖 AI Market Prediction")

model_choice = st.selectbox(
    "Choose ML Model",
    ["Random Forest", "Logistic Regression"]
)

model_type = "rf" if model_choice == "Random Forest" else "lr"

features_df = create_features(data, avg_sentiment)

# Walk-forward validation
wf_df = walk_forward_validation(features_df, model_type)

prediction = wf_df["prediction"].iloc[-1]
latest_confidence = wf_df["confidence"].iloc[-1]

features_df["prediction"] = wf_df["prediction"]
features_df["confidence"] = wf_df["confidence"]

if pd.isna(prediction):
    st.warning("Not enough data for AI prediction. Use 6mo or 1y.")
    st.stop()

signal = generate_signal(prediction, latest_confidence, threshold=0.60)


col1, col2, col3, col4 = st.columns(4)
col1.metric("Model", model_choice)
col2.metric("Prediction", "Bullish" if prediction == 1 else "Bearish")
col3.metric("Confidence", f"{latest_confidence:.2f}")
col4.metric("Trade Signal", signal)

st.caption("Model evaluated using walk-forward validation")
# ================== PREDICTION DISTRIBUTION ==================
st.subheader("🥧 Prediction Distribution")

pred_counts = features_df["prediction"].value_counts(dropna=True)

labels = []
values = []

if 1 in pred_counts:
    labels.append("Bullish")
    values.append(pred_counts[1])

if 0 in pred_counts:
    labels.append("Bearish")
    values.append(pred_counts[0])

fig_pred_pie = go.Figure(
    data=[
        go.Pie(
            labels=labels,
            values=values,
            hole=0.4
        )
    ]
)

fig_pred_pie.update_layout(
    template="plotly_dark",
    title="Model Prediction Distribution"
)

st.plotly_chart(fig_pred_pie, use_container_width=True)


# ================== BACKTESTING ==================
st.subheader("📉 Strategy Backtesting")

bt_df = backtest_strategy(features_df, cost=0.001)



fig_bt = go.Figure()
fig_bt.add_trace(go.Scatter(y=bt_df["cum_strategy"], name="AI Strategy"))
fig_bt.add_trace(go.Scatter(y=bt_df["cum_market"], name="Buy & Hold"))

fig_bt.update_layout(
    template="plotly_dark",
    xaxis_title="Time",
    yaxis_title="Cumulative Return",
)

st.plotly_chart(fig_bt, use_container_width=True)
st.subheader("🔥 Volatility Regime Analysis")

# Create volatility regimes using quantiles
bt_df["vol_regime"] = pd.qcut(
    bt_df["volatility"],
    q=3,
    labels=["Low Volatility", "Medium Volatility", "High Volatility"]
)
regime_returns = (
    bt_df
    .groupby("vol_regime")["strategy_return"]
    .mean()
    .reset_index()
)
fig_regime = go.Figure(
    data=go.Heatmap(
        z=[regime_returns["strategy_return"]],
        x=regime_returns["vol_regime"],
        y=["Avg Strategy Return"],
        colorscale="RdYlGn",
        zmid=0
    )
)

fig_regime.update_layout(
    template="plotly_dark",
    title="Strategy Performance Across Volatility Regimes"
)

st.plotly_chart(fig_regime, use_container_width=True)


# ================== PIE CHARTS FOR REPORT ==================

# Prediction distribution
pred_counts = features_df["prediction"].value_counts(dropna=True)

pred_labels = []
pred_values = []

if 1 in pred_counts:
    pred_labels.append("Bullish")
    pred_values.append(pred_counts[1])

if 0 in pred_counts:
    pred_labels.append("Bearish")
    pred_values.append(pred_counts[0])

report_assets.save_pie_chart(
    pred_labels,
    pred_values,
    "Prediction Distribution",
    "prediction_distribution.png"
)

# Trade outcome distribution
trade_outcomes = bt_df["strategy_return"].apply(
    lambda x: "Winning" if x > 0 else ("Losing" if x < 0 else "No Trade")
)

outcome_counts = trade_outcomes.value_counts()

report_assets.save_pie_chart(
    outcome_counts.index.tolist(),
    outcome_counts.values.tolist(),
    "Trade Outcome Distribution",
    "trade_outcomes.png"
)


# ================== TRADE OUTCOME DISTRIBUTION ==================
st.subheader("🥧 Trade Outcome Distribution")

trade_outcomes = bt_df["strategy_return"].apply(
    lambda x: "Winning Trade" if x > 0 else ("Losing Trade" if x < 0 else "No Trade")
)

outcome_counts = trade_outcomes.value_counts()

fig_trade_pie = go.Figure(
    data=[
        go.Pie(
            labels=outcome_counts.index,
            values=outcome_counts.values,
            hole=0.4
        )
    ]
)

fig_trade_pie.update_layout(
    template="plotly_dark",
    title="Trade Outcome Distribution"
)

st.plotly_chart(fig_trade_pie, use_container_width=True)


# ================== RISK METRICS ==================
st.subheader("📊 Risk Metrics")

sharpe = sharpe_ratio(bt_df["strategy_return"])
drawdown = max_drawdown(bt_df["cum_strategy"])

col1, col2 = st.columns(2)
col1.metric("Sharpe Ratio", f"{sharpe:.2f}")
col2.metric("Max Drawdown", f"{drawdown:.2%}")

# ================== RESEARCH REPORT ==================
st.subheader("📄 Research Report")

if st.button("Generate Full Research PDF"):
    report_assets.save_equity_curve(bt_df)

    report_generator.generate_research_report(
        filename=f"{symbol}_research_report.pdf",
        symbol=symbol,
        model_name=model_choice,
        prediction="Bullish" if prediction == 1 else "Bearish",
        signal=signal,
        sharpe=sharpe,
        drawdown=drawdown,
        equity_curve_path="equity_curve.png",
    )


    with open(f"{symbol}_research_report.pdf", "rb") as f:
        st.download_button(
            "📥 Download Full Research Report",
            f,
            file_name=f"{symbol}_research_report.pdf",
            mime="application/pdf",
        )

# ================== NEWS DISPLAY ==================
st.subheader("🗞️ Top News")
for article in articles[:5]:
    st.markdown(f"**{article['title']}**")
    st.caption(article["source"]["name"])
    st.write(article.get("description", ""))
    st.markdown("---")
