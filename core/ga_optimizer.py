import random

FEATURES = [
    "return",
    "volatility",
    "sentiment",
    "ma5",
    "ma10",
    "momentum",
    "volume_change",
    "ma_ratio",
    "price_vs_ma5"
]

def random_chromosome():
    return [
        random.randint(0, 1)
        for _ in FEATURES
    ]
