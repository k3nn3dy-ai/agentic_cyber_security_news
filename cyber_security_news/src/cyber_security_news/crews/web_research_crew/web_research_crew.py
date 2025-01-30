from crewai import Agent, Crew, Process, Task
from crewai_tools import WebsiteSearchTool, Tool
from crewai.project import CrewBase, agent, crew, task
from datetime import datetime
from crewai_tools import FileReadTool
from pydantic import BaseModel
from src.cyber_security_news.tools.google_search import GoogleNewsSearch
from src.cyber_security_news.tools.crew_cve_tool import fetch_cve_data_tool


class WebResearchOutput(BaseModel):
    search_task: str = ""
    filter_task: str = ""
    summarise_task: str = ""
    weekly_overview_task: str = ""

@CrewBase
class WebResearchCrew():
	"""WebResearchCrew crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'
	file_reader_tool = FileReadTool()
	date = datetime.now().strftime('%Y-%m-%d')
	google_search = GoogleNewsSearch()
	results = google_search._run(date)

	@agent
	def web_researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['web_researcher'],
			tools=[self.google_search, fetch_cve_data_tool],
			verbose=True
		)

	@task
	def search_task(self) -> Task:
		return Task(
			config=self.tasks_config['search_task'],
			output_file='search_task.md'
		)

	@task
	def filter_task(self) -> Task:
		return Task(
			config=self.tasks_config['filter_task'],
			output_file='filter_task.md'
		)

	@task
	def summarise_task(self) -> Task:
		return Task(
			config=self.tasks_config['summarise_task'],
			output_file='summarise_task.md'
		)
	
	@task
	def weekly_overview_task(self) -> Task:
		return Task(
			config=self.tasks_config['weekly_overview_task'],
			output_file='weekly_overview_task.md'
		)
	
	@task
	def cisa_kev_task(self) -> Task:
		return Task(
			config=self.tasks_config['cisa_kev_task'],
			output_file='cisa_kev_task.md'
		)
	
	@task
	def set_structured_output(self) -> Task:
		return Task(
			config=self.tasks_config['set_structured_output'],
			output_pydantic=WebResearchOutput
		)
	@crew
	def crew(self) -> Crew:
		"""Creates the WebResearchCrew crew"""

		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			process=Process.sequential,
			verbose=False,
			output_log_file='web_research.log',
		)