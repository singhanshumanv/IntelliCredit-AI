import requests
from llm_config import get_llm

def fetch_company_news(company):

    url = f"https://newsapi.org/v2/everything?q={company}&pageSize=5&apiKey=ee0a2d51e9f14862bdbce164a3bbab17"

    response = requests.get(url)
    data = response.json()

    articles = []

    for article in data.get("articles", []):
        articles.append(article["title"])

    return articles




llm = get_llm()

def analyze_news_risk(company, articles):

    text = "\n".join(articles)

    prompt = f"""
Analyze these news headlines about {company}.

Identify potential financial or legal risks.

Return ONLY 3-5 SHORT bullet points.
Each bullet must be under 12 words.

Headlines:
{text}
"""

    response = llm.invoke(prompt)

    return response.content