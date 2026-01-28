from newsapi import NewsApiClient

NEWS_API_KEY = "85ee2bd2e1154ca9b865f97ebf666a77"

newsapi = NewsApiClient(api_key=NEWS_API_KEY)

def fetch_news(query, page_size=10):
    try:
        articles = newsapi.get_everything(
            q=query,
            language="en",
            sort_by="relevancy",
            page_size=page_size
        )
        return articles["articles"]
    except Exception as e:
        print("News fetch error:", e)
        return []
