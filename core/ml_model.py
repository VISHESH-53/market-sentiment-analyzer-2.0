import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def train_predict(
    df,
    model_type="lr",
    feature_columns=None
):
    """
    Train model and return prediction info.

    Returns:
    prediction,
    probabilities,
    accuracy,
    model_name,
    importances,
    model
    """

    df = df.dropna()

    if feature_columns is None:
        feature_columns = [
            "return",
            "volatility",
            "sentiment"
        ]

    X = df[feature_columns]
    y = df["target"]

    if len(df) < 30:
        return (
            None,
            None,
            None,
            None,
            None,
            None
        )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        shuffle=False
    )

    if model_type == "rf":

        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=5,
            random_state=42
        )

        model_name = "Random Forest"

        model.fit(
            X_train,
            y_train
        )

        importances = model.feature_importances_

    else:

        model = LogisticRegression(
            max_iter=1000
        )

        model_name = "Logistic Regression"

        model.fit(
            X_train,
            y_train
        )

        importances = None

    accuracy = accuracy_score(
        y_test,
        model.predict(X_test)
    )

    proba = model.predict_proba(X)[:, 1]

    prediction = int(
        proba[-1] > 0.5
    )

    return (
        prediction,
        proba,
        accuracy,
        model_name,
        importances,
        model
    )
