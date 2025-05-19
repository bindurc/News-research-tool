import requests
import re
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("NEWSAPI_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

def get_location():
    try:
        data = requests.get("https://ipinfo.io").json()
        return f"{data.get('city', 'Unknown')}, {data.get('country', 'Unknown')}"
    except:
        return "Unknown Location"

def get_weather(location):
    try:
        city = location.split(",")[0]
        res = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        ).json()
        return f"{res['weather'][0]['description'].capitalize()}, {res['main']['temp']}°C"
    except:
        return "Weather unavailable"

def get_news(category):
    params = {"apiKey": API_KEY, "category": category, "country": "us"}
    res = requests.get("https://newsapi.org/v2/top-headlines", params=params)
    return res.json().get("articles", []) if res.status_code == 200 else []

def format_news_report(raw_markdown, location, weather):
    today = datetime.now().strftime("%Y-%m-%d")
    header = f"""
## 🗺️ Location: {location}
### 🌤️ Weather: {weather}
📅 Date: {today}
## 📰 Headline
"""
    image_pattern = r'(https?://\S+\.(?:png|jpg|jpeg|gif|webp))'
    parts = re.split(image_pattern, raw_markdown)

    formatted = header
    for part in parts:
        if re.match(image_pattern, part):
            formatted += f'\n\n<img src="{part}" width="300" style="margin: 1rem 0;" />\n'
        else:
            cleaned = part.replace("🖼️", "").strip()
            formatted += f'\n\n{cleaned}\n'
    return formatted
