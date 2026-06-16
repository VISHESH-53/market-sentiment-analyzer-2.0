from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
    PageBreak
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

from datetime import datetime
import os


def safe_image(path, width, height, styles):

    if path and os.path.exists(path):

        try:
            return Image(
                path,
                width=width,
                height=height
            )

        except Exception:

            return Paragraph(
                f"Error loading image: {path}",
                styles["Normal"]
            )

    return Paragraph(
        f"Image not available: {path}",
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
    equity_curve_path,

    # Optional future parameters
    confidence=None,
    selected_features=None,
    strategy_return=None,
    market_return=None,

    feature_importance_path=None,
    confidence_chart_path=None,
    ga_features_path=None
):

    styles = getSampleStyleSheet()

    story = []

    doc = SimpleDocTemplate(
        filename,
        pagesize=A4
    )

    if selected_features is None:
        selected_features = []

    sharpe_text = (
        f"{sharpe:.2f}"
        if sharpe is not None
        else "N/A"
    )

    drawdown_text = (
        f"{drawdown:.2%}"
        if drawdown is not None
        else "N/A"
    )

    # =========================
    # TITLE PAGE
    # =========================

    story.append(
        Paragraph(
            "Quantitative Market Sentiment Analyzer<br/>"
            "<font size=14>"
            "AI-Based Trading Strategy Research Report"
            "</font>",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 30))

    story.append(
        Paragraph(
            f"<b>Asset:</b> {symbol}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Model:</b> {model_name}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Generated:</b> "
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 20))

    # =========================
    # EXECUTIVE DASHBOARD
    # =========================

    dashboard_data = [
        ["Metric", "Value"],
        ["Prediction", prediction],
        ["Signal", signal],
        [
            "Confidence",
            f"{confidence:.2%}"
            if confidence is not None
            else "N/A"
        ],
        ["Sharpe Ratio", sharpe_text],
        ["Max Drawdown", drawdown_text]
    ]

    dashboard = Table(dashboard_data)

    dashboard.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("ALIGN", (0, 0), (-1, -1), "CENTER")
        ])
    )

    story.append(dashboard)

    story.append(PageBreak())

    # =========================
    # EXECUTIVE SUMMARY
    # =========================

    story.append(
        Paragraph(
            "1. Executive Summary",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            f"""
            The system forecasts a
            <b>{prediction}</b> market outlook and
            generates a <b>{signal}</b> signal using
            quantitative price analysis,
            sentiment intelligence,
            machine learning,
            and evolutionary optimization.
            """,
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 12))

    # =========================
    # METHODOLOGY
    # =========================

    story.append(
        Paragraph(
            "2. Data & Methodology",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            """
            Historical market data was combined
            with sentiment extracted from
            financial news sources.

            Machine learning models were
            evaluated using walk-forward
            validation to minimize look-ahead
            bias and improve robustness.
            """,
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 12))

    # =========================
    # EVOLUTIONARY SECTION
    # =========================

    story.append(
        Paragraph(
            "3. Evolutionary Optimization",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            """
            A Genetic Algorithm was used
            to identify informative
            predictive features and improve
            model performance.
            """,
            styles["Normal"]
        )
    )

    if selected_features:

        for feature in selected_features:

            story.append(
                Paragraph(
                    f"✓ {feature}",
                    styles["Normal"]
                )
            )

    story.append(Spacer(1, 10))

    if ga_features_path:
        story.append(
            safe_image(
                ga_features_path,
                400,
                250,
                styles
            )
        )

    # =========================
    # MODEL
    # =========================

    story.append(
        Paragraph(
            "4. Model Architecture",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            f"""
            Model Used:
            <b>{model_name}</b>

            The model learns relationships
            between price behavior,
            sentiment information,
            and engineered technical features.
            """,
            styles["Normal"]
        )
    )

    if feature_importance_path:

        story.append(
            safe_image(
                feature_importance_path,
                450,
                250,
                styles
            )
        )

    # =========================
    # CONFIDENCE
    # =========================

    story.append(
        Paragraph(
            "5. Prediction Confidence",
            styles["Heading2"]
        )
    )

    if confidence_chart_path:

        story.append(
            safe_image(
                confidence_chart_path,
                400,
                120,
                styles
            )
        )

    # =========================
    # BACKTESTING
    # =========================

    story.append(
        Paragraph(
            "6. Backtesting Results",
            styles["Heading2"]
        )
    )

    story.append(
        safe_image(
            equity_curve_path,
            450,
            300,
            styles
        )
    )

    # =========================
    # RISK
    # =========================

    story.append(
        Paragraph(
            "7. Risk Analysis",
            styles["Heading2"]
        )
    )

    if drawdown is not None:

        if drawdown > -0.10:
            risk_level = "LOW"

        elif drawdown > -0.20:
            risk_level = "MEDIUM"

        else:
            risk_level = "HIGH"

    else:
        risk_level = "UNKNOWN"

    story.append(
        Paragraph(
            f"""
            Risk Classification:
            <b>{risk_level}</b><br/><br/>

            Sharpe Ratio:
            <b>{sharpe_text}</b><br/>

            Maximum Drawdown:
            <b>{drawdown_text}</b>
            """,
            styles["Normal"]
        )
    )

    # =========================
    # BENCHMARK TABLE
    # =========================

    story.append(
        Paragraph(
            "8. Strategy Benchmark",
            styles["Heading2"]
        )
    )

    table_data = [
        ["Metric", "AI Strategy", "Buy & Hold"],
        [
            "Return",
            (
                f"{strategy_return:.2%}"
                if strategy_return is not None
                else "N/A"
            ),
            (
                f"{market_return:.2%}"
                if market_return is not None
                else "N/A"
            )
        ],
        ["Sharpe Ratio", sharpe_text, "-"],
        ["Max Drawdown", drawdown_text, "-"]
    ]

    table = Table(table_data)

    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("ALIGN", (0, 0), (-1, -1), "CENTER")
        ])
    )

    story.append(table)

    # =========================
    # AI COMMENTARY
    # =========================

    story.append(
        Paragraph(
            "9. AI Commentary",
            styles["Heading2"]
        )
    )

    commentary = f"""
    The model currently forecasts a
    {prediction.lower()} market environment.

    The generated trading signal is
    {signal}.

    The system combines sentiment
    analysis, quantitative features,
    machine learning,
    and evolutionary optimization
    to support trading decisions.
    """

    story.append(
        Paragraph(
            commentary,
            styles["Normal"]
        )
    )

    # =========================
    # CONCLUSION
    # =========================

    story.append(
        Paragraph(
            "10. Conclusion",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            """
            The results demonstrate the
            effectiveness of integrating
            sentiment intelligence,
            machine learning,
            risk analysis,
            and evolutionary computation
            into a unified market
            prediction framework.
            """,
            styles["Normal"]
        )
    )

    # =========================
    # BUILD PDF
    # =========================

    doc.build(story)
