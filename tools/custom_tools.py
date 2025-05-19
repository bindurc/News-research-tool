from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime
from langchain_tavily import TavilySearch as TavilyLangTool
from duckduckgo_search import DDGS
import requests
import os

# --- Tavily Search Tool ---

class TavilySearchInput(BaseModel):
    query: str = Field(..., description="Search query")

class TavilySearchTool(BaseTool):
    name: str = "Tavily Search Tool"
    description: str = "Useful for performing web search with Tavily"
    args_schema: Type[BaseModel] = TavilySearchInput

    def _run(self, query: str) -> str:
        return TavilyLangTool().run(query)


# --- News Search Tool ---

class NewsSearchInput(BaseModel):
    query: str = Field(..., description="News search query")

class NewsSearchTool(BaseTool):
    name: str = "News Search Tool"
    description: str = "Searches recent news articles about the topic using DuckDuckGo (past week)"
    args_schema: Type[BaseModel] = NewsSearchInput

    def _run(self, query: str) -> list:
        with DDGS() as ddgs:
            return list(ddgs.news(query, timelimit="w", max_results=10))


# --- Image Search Tool ---

class ImageSearchInput(BaseModel):
    query: str = Field(..., description="Image search query")

class ImageSearchTool(BaseTool):
    name: str = "Image Search Tool"
    description: str = "Searches relevant images using DuckDuckGo"
    args_schema: Type[BaseModel] = ImageSearchInput

    def _run(self, query: str) -> list:
        with DDGS() as ddgs:
            return list(ddgs.images(
                query=query,
                region='wt-wt',
                safesearch='moderate',
                timelimit='y',
                max_results=10
            ))


# --- Video Search Tool ---

class VideoSearchInput(BaseModel):
    query: str = Field(..., description="Video search query")

class VideoSearchTool(BaseTool):
    name: str = "Video Search Tool"
    description: str = "Searches videos about a topic using DuckDuckGo"
    args_schema: Type[BaseModel] = VideoSearchInput

    def _run(self, query: str) -> list:
        with DDGS() as ddgs:
            return list(ddgs.videos(
                query=query,
                region='wt-wt',
                safesearch='moderate',
                max_results=10
            ))


# --- NewsAPI Tool (Optional) ---

class NewsAPIFetcher(BaseTool):
    name: str = "NewsAPI Fetcher Tool"
    description: str = "Fetches top categorized news articles from NewsAPI.org"

    def _run(self, topic: str) -> list | str:
        api_key = os.getenv("NEWSAPI_API_KEY")
        if not api_key:
            return "Error: API key is missing. Please set NEWSAPI_API_KEY in your .env file."

        url = (
            f"https://newsapi.org/v2/top-headlines"
            f"?q={topic}&language=en&pageSize=5&country=us&apiKey={api_key}"
        )

        response = requests.get(url)
        if response.status_code != 200:
            return f"Error: NewsAPI returned status {response.status_code} - {response.text}"

        data = response.json()
        articles = data.get("articles", [])
        if not articles:
            return "No articles found."

        return [
            {
                "title": article.get("title"),
                "description": article.get("description"),
                "url": article.get("url"),
                "urlToImage": article.get("urlToImage"),
                "publishedAt": article.get("publishedAt"),
                "content": article.get("content") or "Content not provided.",
                "category": topic
            }
            for article in articles
        ]

