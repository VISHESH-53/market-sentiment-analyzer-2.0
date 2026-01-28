def generate_signal(prediction, confidence):
    if prediction == 1 and confidence >= 0.60:
        return "🟢 BUY"
    elif prediction == 0 and confidence >= 0.60:
        return "🔴 SELL"
    else:
        return "🟡 HOLD"
