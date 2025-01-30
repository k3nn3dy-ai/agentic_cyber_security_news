#!/usr/bin/env python

import warnings
import os
# import agentops
from pydantic import BaseModel
from datetime import datetime
from crewai.flow.flow import Flow, listen, start, or_, router
from .crews.web_research_crew.web_research_crew import WebResearchCrew
from .crews.newsroom_crew.newsroom_crew import NewsroomCrew
from .crews.editor.editor import Editor

# Filter out the specific warning before initializing AgentOps
warnings.filterwarnings("ignore", message="Overriding already configured TracerProvider")

# agentops_key = os.getenv("AGENTOPS_KEY")
# agentops.init(agentops_key)

def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")

class ContentTrigger(BaseModel):
    date: str = get_current_date()
    newsroom_report: str = ""
    retrycount: int = 1
    is_acceptable: bool = False
    editors_feedback: str = ""
    filter_task: str = ""
    search_task: str = ""
    summarise_task: str = ""
    weekly_overview_task: str = ""


class CyberSecurityNewsFlow(Flow[ContentTrigger]):

    @start()
    def start_flow(self):
        print("🚀 Cyber Security News Flow Started, please wait... ⚡")

    @listen(start_flow)
    def carry_out_research(self):
        print("🔍 Gathering this week's cyber security news! 📰")
        result = (
            WebResearchCrew()
            .crew()
            .kickoff(inputs={"date": self.state.date})
        )

        print("✅ Internet research completed!!! 🌐")
        self.state.filter_task = result["filter_task"]
        # print(f"🔍 Filter task: {self.state.filter_task}")
        self.state.search_task = result["search_task"]
        # print(f"🔍 Search task: {self.state.search_task}")
        self.state.summarise_task = result["summarise_task"]
        # print(f"🔍 Summarise task: {self.state.summarise_task}")
        self.state.weekly_overview_task = result["weekly_overview_task"]
        # print(f"🔍 Weekly overview task: {self.state.weekly_overview_task}")

    @listen("Not Acceptable")
    def retry_newsroom_review(self):
        print("🔄 Retrying newsroom review... 📝")
        self.state.retrycount += 1

    @listen(or_(carry_out_research, retry_newsroom_review))
    def newsroom_review(self):
        print("📝 Carrying out a review of this week's cyber security news! 📊")
        result = (
            NewsroomCrew()
            .crew()
            .kickoff(inputs={
                "date": self.state.date, 
                "editors_feedback": self.state.editors_feedback, 
                "newsroom_report": self.state.newsroom_report, 
                })
        )
        print("✨ Newsroom review completed!!! 📋")
        self.state.newsroom_report = result.raw

    @router(newsroom_review)
    def editor_review(self):
        print("👀 Editor reviewing this week's cyber security news! ✍️")
        result = (
            Editor()
            .crew()
            .kickoff(inputs={"date": self.state.date, "newsroom_report": self.state.newsroom_report})
        )
        self.state.editors_feedback = result["editor_feedback"]
        self.state.is_acceptable = result["is_acceptable"]
        print(f"🎯 Is the report of an acceptable standard? {self.state.is_acceptable}")
        print(f"💬 Editor feedback: {self.state.editors_feedback}")
        
        # Auto-accept if retry count is 3 or more
        if self.state.retrycount >= 3:
            print("🔄 Maximum retry attempts reached (3) - automatically accepting report")
            return "Acceptable"
            
        if self.state.is_acceptable:
            # print("✅ Report is of an acceptable standard! 📢")
            return "Acceptable"
        else:
            print("⚠️ Report is not of an acceptable standard. 📢")
            return "Not Acceptable"
        
    @listen("Acceptable")
    def publish_report(self):
        print("✅ Report is of an acceptable standard! 📢")

def kickoff():
    cyber_security_flow = CyberSecurityNewsFlow()
    cyber_security_flow.kickoff()


def plot():
    cyber_security_flow = CyberSecurityNewsFlow()
    cyber_security_flow.plot()


if __name__ == "__main__":
    kickoff()
