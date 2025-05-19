from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agents.ai_agent import run_ai_crew
from agents.financial_agent import fetch_ai_news
from utils.helper import get_news, get_location, get_weather

app = FastAPI(title="PulseWire API")

# CORS (if calling from browser/Streamlit etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Request Models ---
class AgentQuery(BaseModel):
    query: str

# --- Endpoints ---

@app.get("/")
def home():
    return {"message": "Welcome to PulseWire API"}

@app.post("/ai-summary")
def ai_summary(payload: AgentQuery):
    location = get_location()
    weather = get_weather(location)
    result = run_ai_crew(payload.query, location, weather)
    return {"location": location, "weather": weather, "summary": result}

@app.post("/financial-news")
def financial_news(payload: AgentQuery):
    result = fetch_ai_news(payload.query)
    return {"result": result}

@app.get("/top-headlines")
def top_headlines(category: str = Query("general")):
    news = get_news(category)
    return {"category": category, "articles": news}
