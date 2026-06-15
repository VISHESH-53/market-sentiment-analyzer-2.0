import numpy as np

from core.ml_model import train_predict


def walk_forward_validation(
    df,
    model_type="lr",
    train_ratio=0.7,
    feature_columns=None
):
    """
    Walk-forward validation.

    Returns dataframe with:
    prediction
    confidence
    """

    df = df.copy()

    df = (
        df
        .dropna()
        .reset_index(drop=True)
    )

    n = len(df)

    split = int(
        n * train_ratio
    )

    predictions = []
    confidences = []

    for i in range(split, n):

        train_df = df.iloc[:i]

        result = train_predict(
            train_df,
            model_type,
            feature_columns
        )

        if result[0] is None:

            predictions.append(np.nan)
            confidences.append(np.nan)

            continue

        (
            _,
            proba,
            _,
            _,
            _,
            _
        ) = result

        confidence = proba[-1]

        prediction = int(
            confidence > 0.5
        )

        predictions.append(
            prediction
        )

        confidences.append(
            confidence
        )

    df["prediction"] = (
        [np.nan] * split
        + predictions
    )

    df["confidence"] = (
        [np.nan] * split
        + confidences
    )

    return df
