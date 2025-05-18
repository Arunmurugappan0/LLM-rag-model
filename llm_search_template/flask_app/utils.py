import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

def search_articles(query):
    """
    Searches for articles using the Serper API.
    """
    if not SERPER_API_KEY:
        raise ValueError("Missing SERPER_API_KEY")

    url = "https://google.serper.dev/news"
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    data = {"q": query}

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    results = response.json()

    articles = []
    for result in results.get("news", []):
        articles.append({
            "url": result["link"],
            "title": result["title"],
            "snippet": result["snippet"]
        })

    return articles

def fetch_article_content(url):
    """
    Fetches article content by scraping the page.
    """
    try:
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.content, 'html.parser')
        paragraphs = soup.find_all('p')
        content = "\n".join(p.get_text() for p in paragraphs)
        return content.strip()
    except Exception:
        return ""

def concatenate_content(articles):
    """
    Combines article contents into a single string.
    """
    combined = ""
    for article in articles:
        combined += f"\n\n### {article['title']}\n{article.get('content', '')}"
    return combined.strip()

def generate_answer(content, query):
    """
    Uses Gemini API to generate an answer from news content.
    """
    if not GEMINI_API_KEY:
        raise ValueError("Missing GEMINI_API_KEY")

    prompt = f"""
    Here is a collection of information extracted from recent news articles:

    {content}

    Based on this information, answer the following query:
    {query}
    """

    model = genai.GenerativeModel('gemma-3-27b-it')
    response = model.generate_content(prompt)
    return response.text.strip()
