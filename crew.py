from crewai import Agent, Crew, Process, Task, LLM
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileWriterTool
from tools.custom_tools import TavilySearchTool, NewsSearchTool, ImageSearchTool, VideoSearchTool
from dotenv import load_dotenv
import os

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Ensure the correct LLM initialization

assert os.getenv("GOOGLE_APPLICATION_CREDENTIALS") is not None, "GOOGLE_APPLICATION_CREDENTIALS not set!"




load_dotenv()

llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.7,
)


@CrewBase
class AiNews:
    """AiNews crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def News_Aggregator_Agent(self) -> Agent:
        return Agent(
            config=self.agents_config['News_Aggregator_Agent'],
            tools=[TavilySearchTool(), NewsSearchTool()],
            llm=llm,
            verbose=True
        )

    @agent
    def Media_Agent(self) -> Agent:
        return Agent(
            config=self.agents_config['Media_Agent'],
            tools=[TavilySearchTool(), NewsSearchTool(), ImageSearchTool(), VideoSearchTool()],
            llm=llm,
            verbose=True
        )

    @agent
    def Writer_Agent(self) -> Agent:
        return Agent(
            config=self.agents_config['Writer_Agent'],
            tools=[],
            llm=llm,
            verbose=True
        )

    @agent
    def Editor_Agent(self) -> Agent:
        return Agent(
            config=self.agents_config['Editor_Agent'],
            tools=[],
            llm=llm,
            verbose=True
        )

    @agent
    def Publishing_Agent(self) -> Agent:
        return Agent(
            config=self.agents_config['Publishing_Agent'],
            tools=[FileWriterTool()],
            llm=llm,
            verbose=True
        )


    """Tasks"""

    @task
    def News_Aggregator_Agent_task(self) -> Task:
        return Task(
            config=self.tasks_config['News_Aggregator_Agent_task'],
        )


    @task
    def Media_Agent_task(self) -> Task:
        return Task(
            config=self.tasks_config['Media_Agent_task'],
        )

    @task
    def Writer_Agent_task(self) -> Task:
        return Task(
            config=self.tasks_config['Writer_Agent_task'],
        )

    @task
    def Editor_Agent_task(self) -> Task:
        return Task(
            config=self.tasks_config['Editor_Agent_task'],
        )

    @task
    def Publishing_Agent_task(self) -> Task:
        return Task(
            config=self.tasks_config['Publishing_Agent_task'],
        )

    """Crew"""

    @crew
    def crew(self) -> Crew:
        """Creates the AiNews crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
