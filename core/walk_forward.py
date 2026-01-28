import numpy as np
import pandas as pd
from core.ml_model import train_predict

def walk_forward_validation(df, model_type="lr", train_ratio=0.7):
    """
    Perform walk-forward (rolling window) validation.
    Returns dataframe with predictions & confidence.
    """

    df = df.copy()
    df = df.dropna().reset_index(drop=True)

    n = len(df)
    split = int(n * train_ratio)

    predictions = []
    confidences = []

    for i in range(split, n):
        train_df = df.iloc[:i]
        test_df = df.iloc[i:i+1]

        result = train_predict(train_df, model_type)

        if result[0] is None:
            predictions.append(np.nan)
            confidences.append(np.nan)
            continue

        _, proba, _, _, _, _ = result

        # Probability for this step
        confidence = proba[-1]
        prediction = int(confidence > 0.5)

        predictions.append(prediction)
        confidences.append(confidence)

    # Pad beginning with NaN
    df["prediction"] = [np.nan]*split + predictions
    df["confidence"] = [np.nan]*split + confidences

    return df
