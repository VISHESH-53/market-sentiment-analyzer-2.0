import matplotlib.pyplot as plt

def save_equity_curve(bt_df, filename="equity_curve.png"):
    plt.figure(figsize=(6, 4))
    plt.plot(bt_df['cum_strategy'], label="AI Strategy")
    plt.plot(bt_df['cum_market'], label="Buy & Hold")
    plt.legend()
    plt.title("Strategy vs Buy & Hold")
    plt.xlabel("Time")
    plt.ylabel("Cumulative Return")
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
def save_pie_chart(labels, values, title, filename):
    plt.figure(figsize=(4, 4))
    plt.pie(
        values,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90
    )
    plt.title(title)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
