📊 Market Sentiment Analyzer 2.0

A quantitative trading research project that combines financial market data, news sentiment analysis, machine learning, and risk-managed backtesting using walk-forward validation.

This project focuses on risk-adjusted performance, not just prediction accuracy, following professional quantitative research practices.

🚀 Key Features

📈 Market Data Analysis

OHLC price data for stocks & crypto

Interactive candlestick charts (Plotly)

📰 News Sentiment Analysis

Real-time financial news

NLP-based sentiment scoring

🤖 Machine Learning Models

Logistic Regression

Random Forest

Predicts next-day price direction

🔁 Walk-Forward Validation

Rolling, time-consistent model evaluation

Eliminates look-ahead bias

⚖️ Risk-Managed Trading Strategy

Volatility-based position sizing

Confidence-weighted exposure

Transaction costs

Drawdown-based stop-trading rule

📊 Performance Evaluation

Sharpe Ratio

Maximum Drawdown

Buy-and-Hold benchmark comparison

📄 Automated Research Report

PDF generation with equity curve

Research-style structure and metrics

🧠 Why This Project Is Different

Most ML trading projects optimize accuracy.
This project optimizes risk-adjusted returns.

Key principles applied:

Prediction ≠ Strategy

Accuracy ≠ Profitability

Risk management is mandatory

Walk-forward validation over static backtests

🗂️ Project Structure
market-sentiment-analyzer-2.0/
│
├── app.py
├── README.md
├── requirements.txt
│
├── core/
│   ├── __init__.py
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

⚙️ How It Works (Pipeline)

Fetch market price data

Fetch financial news

Compute sentiment scores

Engineer features

Returns

Volatility

Sentiment

Walk-forward model training & prediction

Generate trading signals

Risk-managed backtesting

Evaluate performance

Generate research PDF report

📈 Example Metrics (TSLA – Sample Run)
Metric	Value
Model Accuracy	~0.48
Sharpe Ratio	~0.7 – 1.1
Max Drawdown	~30%
Validation	Walk-Forward

Even with sub-50% accuracy, the strategy achieves positive risk-adjusted returns through selective trading and strict risk control.

▶️ How to Run
1️⃣ Clone the repository
git clone https://github.com/<your-username>/market-sentiment-analyzer-2.0.git
cd market-sentiment-analyzer-2.0

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Run the app
streamlit run app.py

📄 Generate Research Report

Inside the app:

Select asset & time period

Choose ML model

Run analysis

Click Generate Full Research PDF

A complete research-style report will be generated automatically.

⚠️ Disclaimer

This project is for educational and research purposes only.
It does not constitute financial or investment advice.

🎓 Skills Demonstrated

Data Science

Machine Learning

Time-series analysis

NLP & sentiment analysis

Quantitative finance

Risk management

Research reporting

Python engineering

Streamlit deployment

🔮 Future Improvements

Regime detection (bull/bear markets)

Slippage modeling

Portfolio-level optimization

Deep learning models

Live deployment

Multi-asset strategies

👤 Author

Vishesh Agrawal
BTech CSE (Data Science)
Aspiring Quant / Data Scientist
