from datetime import datetime
from  utils.helper import format_news_report

def run_ai_crew(query, location, weather):
    try:
        from crew import AiNews
        result = AiNews().crew().kickoff(inputs={
            'query': query.strip(),
            'date': datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        })

        raw_markdown = getattr(result, "raw", str(result))
        if raw_markdown:
            return format_news_report(raw_markdown, location, weather)
    except Exception as e:
        print(f"Error: {e}")
        return None
