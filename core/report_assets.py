import matplotlib.pyplot as plt
import pandas as pd


# ==========================
# EQUITY CURVE
# ==========================

def save_equity_curve(
    bt_df,
    filename="equity_curve.png"
):
    plt.figure(figsize=(8, 5))

    plt.plot(
        bt_df["cum_strategy"],
        linewidth=2,
        label="AI Strategy"
    )

    plt.plot(
        bt_df["cum_market"],
        linewidth=2,
        label="Buy & Hold"
    )

    plt.title(
        "Strategy Performance Benchmark",
        fontsize=14,
        fontweight="bold"
    )

    plt.xlabel("Time")
    plt.ylabel("Cumulative Return")

    plt.grid(
        alpha=0.3,
        linestyle="--"
    )

    plt.legend()

    plt.tight_layout()
    plt.savefig(
        filename,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


# ==========================
# PREDICTION DISTRIBUTION
# ==========================

def save_pie_chart(
    labels,
    values,
    title,
    filename
):
    plt.figure(figsize=(5, 5))

    plt.pie(
        values,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90
    )

    plt.title(
        title,
        fontsize=14,
        fontweight="bold"
    )

    plt.tight_layout()

    plt.savefig(
        filename,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


# ==========================
# FEATURE IMPORTANCE
# ==========================

def save_feature_importance(
    features,
    importances,
    filename="feature_importance.png"
):

    plt.figure(figsize=(8, 5))

    plt.barh(
        features,
        importances
    )

    plt.title(
        "Feature Importance Analysis",
        fontsize=14,
        fontweight="bold"
    )

    plt.xlabel("Importance Score")

    plt.tight_layout()

    plt.savefig(
        filename,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


# ==========================
# CONFIDENCE GAUGE
# ==========================

def save_confidence_chart(
    confidence,
    filename="confidence.png"
):

    plt.figure(figsize=(6, 1.5))

    plt.barh(
        ["Confidence"],
        [confidence * 100]
    )

    plt.xlim(0, 100)

    plt.title(
        f"Prediction Confidence: {confidence:.1%}"
    )

    plt.tight_layout()

    plt.savefig(
        filename,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


# ==========================
# EVOLUTIONARY FEATURES
# ==========================

def save_ga_features(
    selected_features,
    filename="ga_features.png"
):

    plt.figure(figsize=(6, 4))

    y = list(range(len(selected_features)))

    plt.barh(
        y,
        [1] * len(selected_features)
    )

    plt.yticks(
        y,
        selected_features
    )

    plt.title(
        "Genetic Algorithm Selected Features"
    )

    plt.tight_layout()

    plt.savefig(
        filename,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()
