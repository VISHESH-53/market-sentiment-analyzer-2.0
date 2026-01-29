def generate_signal(prediction, confidence):
    if prediction == 1:
        return "BUY"
    elif prediction == 0:
        return "SELL"
    else:
        return "HOLD"
