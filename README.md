

# 📊 Market Sentiment Analyzer 2.0

**Quantitative trading research project** combining **market data**, **news sentiment**, **machine learning**, and **risk-managed backtesting** using **walk-forward validation**.

> Focuses on **risk-adjusted performance**, not just prediction accuracy.

---

## 🚀 Features

* 📈 OHLC market data (stocks & crypto)
* 📰 News sentiment analysis (NLP)
* 🤖 ML models

  * Logistic Regression
  * Random Forest
* 🔁 Walk-forward validation (no lookahead bias)
* ⚖️ Risk-managed strategy

  * Volatility-based position sizing
  * Confidence-weighted exposure
  * Transaction costs
  * Drawdown stop rule
* 📊 Performance metrics

  * Sharpe Ratio
  * Max Drawdown
  * Buy & Hold comparison
* 📄 Automated **research-style PDF report**

---

## 🧠 Why This Project?

Most ML trading projects optimize **accuracy**.
This project optimizes **risk-adjusted returns**.

Key principles:

* Prediction ≠ Strategy
* Accuracy ≠ Profitability
* Risk management is essential
* Walk-forward validation over static backtests

---

## 🗂️ Project Structure

```
market-sentiment-analyzer-2.0/
│
├── app.py
├── README.md
├── requirements.txt
│
├── core/
│   ├── fetch_market_data.py
│   ├── fetch_news.py
│   ├── sentiment.py
│   ├── feature_engineering.py
│   ├── ml_model.py
│   ├── walk_forward.py
│   ├── backtest.py
│   ├── trading_signal.py
│   ├── risk_metrics.py
│   ├── report_assets.py
│   └── report_generator.py
│
└── .gitignore
```

---

## ⚙️ How It Works

1. Fetch market price data
2. Fetch financial news
3. Compute sentiment scores
4. Engineer features (returns, volatility, sentiment)
5. Walk-forward ML predictions
6. Generate trading signals
7. Risk-managed backtesting
8. Evaluate performance
9. Generate research PDF

---

## 📈 Sample Results (TSLA)

| Metric       | Value        |
| ------------ | ------------ |
| Accuracy     | ~0.48        |
| Sharpe Ratio | ~0.7 – 1.1   |
| Max Drawdown | ~30%         |
| Validation   | Walk-Forward |

> Even with sub-50% accuracy, the strategy achieves positive risk-adjusted returns through selective trading and strict risk control.

---

## ▶️ Run Locally

```bash
git clone https://github.com/<your-username>/market-sentiment-analyzer-2.0.git
cd market-sentiment-analyzer-2.0
pip install -r requirements.txt
streamlit run app.py
```

---

## 📄 Research Report

The app can generate a **full research-style PDF** including:

* Strategy description
* Equity curve
* Risk metrics
* Benchmark comparison

---

## ⚠️ Disclaimer

For **educational and research purposes only**.
Not financial or investment advice.

---

## 🎓 Skills Demonstrated

* Machine Learning
* Time-series analysis
* NLP & sentiment analysis
* Quantitative finance
* Risk management
* Python engineering
* Streamlit applications

---

## 👤 Author

**Vishesh Agrawal**
BTech CSE (Data Science)
Aspiring Quant / Data Scientist

---


