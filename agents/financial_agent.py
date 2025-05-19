import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.tools.yfinance import YFinanceTools
from agno.models.google import Gemini

load_dotenv()
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

news_agent = Agent(
    model=Gemini(id="gemini-2.0-flash", grounding=True, api_key=GOOGLE_API_KEY),
    tools=[YFinanceTools(company_news=True)],
    show_tool_calls=False,
    description=(
        "Conduct a comprehensive search across top financial news sources like CNBC, Bloomberg, Reuters, "
        "Yahoo Finance, MarketWatch, NYT Business, and Google News.\n\n"
        "Your goal is to curate the 10 most recent, high-quality financial articles relevant to \"{query}\".\n"
        "Ensure:\n"
        "- Articles are from the past 7 days.\n"
        "- Sources are trustworthy with high editorial standards.\n"
        "- Content is relevant and free of sensationalism or clickbait.\n"
        "- Each article includes an image (if available), timestamp, and a clear summary.\n\n"
        "Extract and display the following metadata for each article:\n"
        "- 📰 Headline\n"
        "- 🕒 Timestamp\n"
        "- 📝 Summary\n"
        "- 🔗 URL\n"
        "- 🏷️ Publisher"
    ),
    instructions=["Format your response in markdown with bullet points or tables."]
)

def fetch_ai_news(query: str) -> str:
    response = news_agent.run(query)
    return response.content
