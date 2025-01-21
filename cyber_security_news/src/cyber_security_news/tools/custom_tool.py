from crewai_tools import BaseTool
from langchain_community.tools import ShellTool

class CustomShellTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="ShellTool",
            func=self.execute_shell_command,
            description="Executes shell commands using Langchain's ShellTool."
        )
        self._shell_tool = ShellTool()

    def execute_shell_command(self, command: str) -> str:
        return self._shell_tool.run(command)

    def _run(self, *args, **kwargs):
        command = kwargs.get('command', '')
        return self.execute_shell_command(command)