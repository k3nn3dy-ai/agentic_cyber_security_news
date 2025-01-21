#!/usr/bin/env python

from pydantic import BaseModel
from datetime import datetime
from crewai.flow.flow import Flow, listen, start
from .crews.web_research_crew.web_research_crew import WebResearchCrew
from .crews.newsroom_crew.newsroom_crew import NewsroomCrew
from .crews.editor.editor import Editor

def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")

class ContentTrigger(BaseModel):
    date: str = get_current_date()
    research_results: str = ""
    editors_feedback: str = ""
    newsroom_report: str = ""
    retrycount: int = 0
    is_acceptable: bool = False

class CyberSecurityNewsFlow(Flow[ContentTrigger]):

    @start()
    def start_flow(self):
        print("Cyber Security News Flow Started, please wait...")

    @listen(start_flow)
    def carry_out_research(self):
        print("Gathering this week's cyber security news!")
        result = (
            WebResearchCrew()
            .crew()
            .kickoff(inputs={"date": self.state.date})
        )

        print("Internet research completed!!!", result.raw)
        self.state.research_results = result.raw

    @listen(carry_out_research)
    def newsroom_review(self):
        print("Carrying out a review of this week's cyber security news!")
        result = (
            NewsroomCrew()
            .crew()
            .kickoff(inputs={"date": self.state.date, "research_results": self.state.research_results, "editors_feedback": self.state.editors_feedback})
        )
        print("Newsroom review completed!!!", result.raw)
        self.state.newsroom_report = result.raw
        self.state.retrycount += 1

    @listen(newsroom_review)
    def editor_review(self):
        print("Carrying out a review of this week's cyber security news!")
        result = (
            Editor()
            .crew()
            .kickoff(inputs={"date": self.state.date, "newsroom_report": self.state.newsroom_report})
        )
        print("Editor review completed!!!", result.raw)
        self.state.editors_feedback = result["editor_feedback"]
        self.state.is_acceptable = result["is_acceptable"]
        print(f"Is the report of an acceptable standard? {self.state.is_acceptable}")
        print(f"Editor feedback: {self.state.editors_feedback}")
        
        # If not acceptable and under 3 retries, trigger newsroom review again
        if not self.state.is_acceptable and self.state.retrycount < 3:
            print(f"Report needs revision. Attempt {self.state.retrycount + 1}/3")
            self.newsroom_review()
        elif not self.state.is_acceptable:
            print("Maximum retries reached. Publishing report as is.")


def kickoff():
    cyber_security_flow = CyberSecurityNewsFlow()
    cyber_security_flow.kickoff()


def plot():
    cyber_security_flow = CyberSecurityNewsFlow()
    cyber_security_flow.plot()


if __name__ == "__main__":
    kickoff()
