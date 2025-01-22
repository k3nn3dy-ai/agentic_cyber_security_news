from crewai import Agent, Crew, Process, Task
from pydantic import BaseModel
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool

class EditorOutput(BaseModel):
    is_acceptable: bool
    editor_feedback: str

@CrewBase
class Editor():
	"""Editor crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'
	file_reader_tool = FileReadTool()

	@agent
	def newsroom_editor(self) -> Agent:
		return Agent(
			config=self.agents_config['newsroom_editor'],
			tools=[self.file_reader_tool],
			verbose=True
		)

	@task
	def editorial_review(self) -> Task:
		return Task(
			config=self.tasks_config['editorial_review'],
			output_pydantic=EditorOutput
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Editor crew"""
		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			process=Process.sequential,
			verbose=True,
			output_log_file='editor.log',
		)