from crewai import Agent, Crew, Process, Task
from crewai_tools import WebsiteSearchTool, Tool
from crewai.project import CrewBase, agent, crew, task
from datetime import datetime
from crewai_tools import FileReadTool
from pydantic import BaseModel

class WebResearchOutput(BaseModel):
    search_task: str = ""
    filter_task: str = ""
    summarise_task: str = ""
    trend_analysis_task: str = ""
    weekly_overview_task: str = ""


@CrewBase
class WebResearchCrew():
	"""WebResearchCrew crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'
	news_sources = WebsiteSearchTool(
					website = str([
				"https://www.theregister.com/security",
				"https://thehackernews.com",
				"https://www.bleepingcomputer.com",
				"https://threatpost.com",
				"https://krebsonsecurity.com",
				"https://www.darkreading.com",
				"https://www.csoonline.com",
				"https://www.securityweek.com",
				"https://www.schneier.com",
				"https://www.helpnetsecurity.com",
				"https://www.infosecurity-magazine.com",
				"https://www.welivesecurity.com",
				"https://www.cyberscoop.com",
				"https://www.scmagazine.com",
				"https://securityboulevard.com",
				"https://arstechnica.com/security",
				"https://techcrunch.com/tag/security",
				"https://cisomag.eccouncil.org",
				"https://securityintelligence.com",
				"https://thecyberwire.com"
			]),
        description="Search for the latest cybersecurity news stories from trusted sources. only search for stories that are within the last 7 days for the date {date}."
    )
	file_reader_tool = FileReadTool()
	date = datetime.now().strftime('%Y-%m-%d')

	@agent
	def web_researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['web_researcher'],
			tools=[self.news_sources]
		)

	@task
	def search_task(self) -> Task:
		return Task(
			config=self.tasks_config['search_task'],
			output_file='search_task.md',
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
	def trend_analysis_task(self) -> Task:
		return Task(
			config=self.tasks_config['trend_analysis_task'],
			output_file='trend_analysis_task.md'
		)
	
	@task
	def weekly_overview_task(self) -> Task:
		return Task(
			config=self.tasks_config['weekly_overview_task'],
			output_pydantic=WebResearchOutput
		)
	
	@crew
	def crew(self) -> Crew:
		"""Creates the WebResearchCrew crew"""

		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			process=Process.sequential,
			verbose=True,
			output_log_file='web_research.log',
		)