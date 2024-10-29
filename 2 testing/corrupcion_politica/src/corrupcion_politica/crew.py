import os
from crewai import Agent, Crew, Process, Task # type: ignore
from crewai.project import CrewBase, agent, crew, task # type: ignore

# Check our tools documentations for more information on how to use them
from crewai_tools import SerperDevTool, ScrapeWebsiteTool # type: ignore

# Define LLM

os.environ['OPENAI_MODEL_NAME'] = 'gpt-4o-mini'
groq_llm = "groq/llama-3.1-70b-versatile"

@CrewBase
class CorrupcionPoliticaCrew():
    """Corrupcion_Politica Crew"""

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            tools=[SerperDevTool(),ScrapeWebsiteTool()],
            verbose=True,
            llm=groq_llm
        )

    @agent
    def corruption_journalist(self) -> Agent:
        return Agent(
            config=self.agents_config['corruption_journalist'],
            tools=[SerperDevTool(),ScrapeWebsiteTool()],
            verbose=True,
            llm=groq_llm
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['reporting_analyst'],
            verbose=True,
            llm=groq_llm
        )

    @task
    def research_elections_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_elections_task'],
        )

    @task
    def research_corruption_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_corruption_task'],
        )

    @task
    def research_good_projects_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_good_projects_task'],
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'],
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Test0 crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
