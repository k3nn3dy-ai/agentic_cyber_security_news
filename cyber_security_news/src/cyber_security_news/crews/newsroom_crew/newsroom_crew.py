from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool

@CrewBase
class NewsroomCrew():
	"""NewsroomCrew crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	file_reader_tool = FileReadTool()

	@agent
	def report_writer(self) -> Agent:
		return Agent(
			config=self.agents_config['report_writer'],
			tools=[self.file_reader_tool],
			verbose=True
		)
		
	@task
	def research_report(self) -> Task:
		return Task(
			config=self.tasks_config['research_report'],
			output_file='weekly_cyber_security_news_report.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the NewsroomCrew crew"""
		
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
		)
