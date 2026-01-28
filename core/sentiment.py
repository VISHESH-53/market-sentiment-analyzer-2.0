from textblob import TextBlob

def analyze_sentiment(text):
    if not text:
        return 0
    return TextBlob(text).sentiment.polarity

def get_sentiment_label(score):
    if score > 0.1:
        return "🟢 Bullish"
    elif score < -0.1:
        return "🔴 Bearish"
    else:
        return "🟡 Neutral"
