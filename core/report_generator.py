from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from datetime import datetime
import os


def safe_image(path, width, height, styles):

    if path and os.path.exists(path):

        try:
            return Image(path, width=width, height=height)

        except Exception:

            return Paragraph(
                f"Error loading image : {path}",
                styles["Normal"]
            )

    return Paragraph(
        f"Image not available : {path}",
        styles["Normal"]
    )


def generate_research_report(
    filename,
    symbol,
    model_name,
    prediction,
    signal,
    sharpe,
    drawdown,
    equity_curve_path
):

    styles = getSampleStyleSheet()
    story = []

    doc = SimpleDocTemplate(
        filename,
        pagesize=A4
    )

    # ---------- TITLE PAGE ----------

    story.append(Paragraph(
        "Quantitative Market Sentiment Analyzer<br/>"
        "<font size=14>AI-Based Trading Strategy Research Report</font>",
        styles["Title"]
    ))

    story.append(Spacer(1,40))

    story.append(
        Paragraph(f"<b>Asset:</b> {symbol}",styles["Normal"])
    )

    story.append(
        Paragraph(f"<b>Model:</b> {model_name}",styles["Normal"])
    )

    story.append(
        Paragraph(
            f"<b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            styles["Normal"]
        )
    )

    story.append(PageBreak())

    # ---------- EXECUTIVE SUMMARY ----------

    story.append(
        Paragraph("1. Executive Summary",styles["Heading2"])
    )

    story.append(
        Paragraph(
            "This report presents a quantitative trading framework combining market price "
            "data with NLP-based news sentiment. Machine learning is used to predict next-day "
            "price direction and generate trading signals evaluated using risk-adjusted metrics.",
            styles["Normal"]
        )
    )

    story.append(Spacer(1,12))

    # ---------- METHODOLOGY ----------

    story.append(
        Paragraph("2. Data & Methodology",styles["Heading2"])
    )

    story.append(
        Paragraph(
            "Historical OHLC price data was sourced from Yahoo Finance. Financial news was "
            "processed using sentiment polarity scoring. Features were engineered from both "
            "price action and sentiment and fed into a supervised learning model.",
            styles["Normal"]
        )
    )

    story.append(Spacer(1,12))

    # ---------- FEATURES ----------

    story.append(
        Paragraph("3. Feature Engineering",styles["Heading2"])
    )

    story.append(
        Paragraph(
            "Features include daily returns (momentum), rolling volatility (risk proxy), "
            "and aggregated sentiment scores. The target variable represents next-day price "
            "direction.",
            styles["Normal"]
        )
    )

    story.append(Spacer(1,12))

    # ---------- MODEL ----------

    story.append(
        Paragraph("4. Model Architecture",styles["Heading2"])
    )

    story.append(
        Paragraph(
            "A Random Forest classifier was employed due to its ability to model non-linear "
            "relationships and robustness against noisy financial data.",
            styles["Normal"]
        )
    )

    story.append(Spacer(1,12))

    # ---------- STRATEGY ----------

    story.append(
        Paragraph("5. Trading Strategy",styles["Heading2"])
    )

    story.append(
        Paragraph(
            "Predictions are converted into BUY, SELL, or HOLD signals using confidence "
            "thresholds. The strategy avoids overtrading and focuses on high-confidence signals.",
            styles["Normal"]
        )
    )

    story.append(Spacer(1,12))

    # ---------- BACKTESTING ----------

    story.append(
        Paragraph("6. Backtesting Results",styles["Heading2"])
    )

    story.append(
        Paragraph(
            "The strategy was backtested against a Buy-and-Hold benchmark with no lookahead "
            "bias. The following equity curve compares cumulative performance.",
            styles["Normal"]
        )
    )

    story.append(Spacer(1,12))

    story.append(
        safe_image(equity_curve_path,400,300,styles)
    )

    story.append(Spacer(1,12))

    # ---------- DISTRIBUTION ----------

    story.append(PageBreak())

    story.append(
        Paragraph("7. Strategy Distribution Analysis",styles["Heading2"])
    )

    story.append(Spacer(1,12))

    story.append(
        Paragraph(
            "The following charts summarize the model’s behavior in terms of prediction "
            "bias and realized trade outcomes.",
            styles["Normal"]
        )
    )

    story.append(Spacer(1,12))

    story.append(
        Paragraph("Prediction Distribution",styles["Heading3"])
    )

    story.append(
        safe_image("prediction_distribution.png",300,300,styles)
    )

    story.append(Spacer(1,20))

    story.append(
        Paragraph("Trade Outcome Distribution",styles["Heading3"])
    )

    story.append(
        safe_image("trade_outcomes.png",300,300,styles)
    )

    story.append(Spacer(1,20))

    # ---------- RISK ----------

    story.append(
        Paragraph("8. Risk Analysis",styles["Heading2"])
    )

    story.append(
        Paragraph(
            "Sharpe Ratio equation:<br/>"
            "Sharpe = Mean(Return) / Std(Return)<br/><br/>"
            "Maximum Drawdown equation:<br/>"
            "Drawdown = (Peak - Trough) / Peak",
            styles["Normal"]
        )
    )

    story.append(Spacer(1,8))

    sharpe_text = f"{sharpe:.2f}" if sharpe else "N/A"
    drawdown_text = f"{drawdown:.2%}" if drawdown else "N/A"

    story.append(
        Paragraph(
            "Model evaluated using walk-forward validation.<br/><br/>"
            f"<b>Sharpe Ratio:</b> {sharpe_text}<br/>"
            f"<b>Max Drawdown:</b> {drawdown_text}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1,12))

    # ---------- TABLE ----------

    story.append(
        Paragraph("9. Strategy Comparison",styles["Heading2"])
    )

    table_data = [

        ["Metric","AI Strategy","Buy & Hold"],

        ["Sharpe Ratio",sharpe_text,"N/A"],

        ["Max Drawdown",drawdown_text,"Market dependent"],

        ["Decision Type","AI driven","Passive"]

    ]

    table = Table(table_data)

    table.setStyle(

        TableStyle([

            ("BACKGROUND",(0,0),(-1,0),colors.grey),

            ("GRID",(0,0),(-1,-1),1,colors.black),

            ("ALIGN",(1,1),(-1,-1),"CENTER")

        ])

    )

    story.append(table)

    story.append(Spacer(1,12))

    # ---------- LIMITATIONS ----------

    story.append(
        Paragraph("10. Limitations",styles["Heading2"])
    )

    story.append(
        Paragraph(
            "Transaction costs are modeled at a fixed rate; however, slippage and regime "
            "detection are not yet incorporated. News sentiment may also suffer from "
            "reporting delays and headline bias.",
            styles["Normal"]
        )
    )

    story.append(Spacer(1,12))

    # ---------- CONCLUSION ----------

    story.append(
        Paragraph("11. Conclusion & Future Work",styles["Heading2"])
    )

    story.append(
        Paragraph(
            "This research demonstrates the feasibility of integrating sentiment analysis "
            "with machine learning for quantitative trading. By combining walk-forward "
            "validation, confidence-weighted position sizing, and drawdown-based risk "
            "controls, the strategy achieves robust risk-adjusted performance.",
            styles["Normal"]
        )
    )

    # ---------- SAFE BUILD ----------

    try:

        doc.build(story)

    except Exception as e:

        print("PDF generation failed :",str(e))
