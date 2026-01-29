def generate_signal(prediction, confidence, threshold=0.60):
    if confidence is None:
        return "HOLD"

    if confidence >= threshold:
        return "BUY" if prediction == 1 else "SELL"
    else:
        return "HOLD"
