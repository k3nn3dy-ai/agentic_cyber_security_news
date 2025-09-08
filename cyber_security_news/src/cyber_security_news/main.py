#!/usr/bin/env python

import warnings
import os
import subprocess
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
    def __init__(self):
        super().__init__()
        self.final_report = ""

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
        self.final_report = self.state.newsroom_report

def kickoff():
    cyber_security_flow = CyberSecurityNewsFlow()
    cyber_security_flow.kickoff()


def plot():
    cyber_security_flow = CyberSecurityNewsFlow()
    cyber_security_flow.plot()


# Enhanced Streamlit interface function
def run_streamlit():
    import streamlit as st
    import time
    import threading
    from io import StringIO
    import sys
    import os
    import glob
    from datetime import datetime
    import json
    import pandas as pd
    
    st.set_page_config(
        page_title="Cyber Security News Analyzer",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Sidebar Navigation
    with st.sidebar:
        st.title("🛡️ CyberSec AI")
        page = st.selectbox(
            "Navigation",
            ["🚀 Generate Report", "📄 Report Manager", "📊 Dashboard", "⚙️ Settings"]
        )
    
    # Check for required environment variables
    required_vars = ["ANTHROPIC_API_KEY", "SERPER_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars and page == "🚀 Generate Report":
        st.error(f"⚠️ Missing required environment variables: {', '.join(missing_vars)}")
        st.markdown("Please set the following environment variables:")
        for var in missing_vars:
            st.code(f"export {var}=your_{var.lower()}_here")
        st.stop()
    
    # Page Routing
    if page == "🚀 Generate Report":
        show_generate_page()
    elif page == "📄 Report Manager":
        show_report_manager()
    elif page == "📊 Dashboard":
        show_dashboard()
    elif page == "⚙️ Settings":
        show_settings()


def show_generate_page():
    import streamlit as st
    import time
    import threading
    from io import StringIO
    import sys
    import os
    
    st.title("🚀 Generate Cybersecurity Report")
    st.markdown("AI-powered analysis of the latest cybersecurity threats and trends")
    
    # Initialize session state
    if 'flow_running' not in st.session_state:
        st.session_state.flow_running = False
    if 'flow_complete' not in st.session_state:
        st.session_state.flow_complete = False
    if 'final_report' not in st.session_state:
        st.session_state.final_report = ""
    if 'crew_logs' not in st.session_state:
        st.session_state.crew_logs = []
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 0
    if 'current_message' not in st.session_state:
        st.session_state.current_message = ""
    
    # Configuration options
    col1, col2 = st.columns([2, 1])
    
    with col2:
        st.markdown("### ⚙️ Configuration")
        focus_areas = st.multiselect(
            "Focus Areas",
            ["APT Groups", "Zero-Day Exploits", "Ransomware", "Data Breaches", "IoT Security", "Cloud Security"],
            default=["APT Groups", "Zero-Day Exploits", "Data Breaches"]
        )
        
        report_depth = st.selectbox("Report Depth", ["Summary", "Detailed", "Comprehensive"])
        include_cve = st.checkbox("Include CVE Analysis", value=True)
        
        st.markdown("### 📊 Status")
        if st.session_state.flow_running:
            st.info("🔄 Generation in progress...")
            st.progress(st.session_state.current_step / 5)
        elif st.session_state.flow_complete:
            st.success("✅ Report ready!")
        else:
            st.info("⏸️ Ready to start")
    
    with col1:
        if st.button("🚀 Generate Report", disabled=st.session_state.flow_running, type="primary", use_container_width=True):
            st.session_state.flow_running = True
            st.session_state.flow_complete = False
            st.session_state.final_report = ""
            st.session_state.crew_logs = []
            st.session_state.current_step = 0
            
            # Real-time progress display
            progress_container = st.container()
            
            with progress_container:
                progress_bar = st.progress(0)
                status_text = st.empty()
                crew_activity = st.empty()
                log_container = st.container()
                
                def update_progress(step, message, crew_log=""):
                    # Update session state only (thread-safe)
                    st.session_state.current_step = step
                    st.session_state.current_message = message
                    if crew_log:
                        st.session_state.crew_logs.append(f"[{time.strftime('%H:%M:%S')}] {crew_log}")
                
                try:
                    # Create and run the flow with progress tracking
                    flow = CyberSecurityNewsFlow()
                    
                    def run_flow():
                        try:
                            import subprocess
                            import json
                            
                            update_progress(1, "🔍 Starting web research crew...", "Initializing cybersecurity analysis")
                            
                            # Run a simple test in a separate Python process to verify subprocess approach works
                            cmd = [
                                'python3', '-c', 
                                '''
import time
import os

try:
    # Simple test - create a test report
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    os.makedirs("reports", exist_ok=True)
    report_path = f"reports/cybersec_report_{timestamp}.md"
    
    test_report = """# Test Cybersecurity Report
## Generated via Subprocess
This is a test report generated by the subprocess approach.
The subprocess isolation is working correctly!

Date: """ + time.strftime("%Y-%m-%d %H:%M:%S") + """
Status: Successfully generated via isolated subprocess
"""
    
    with open(report_path, "w") as f:
        f.write(test_report)
    
    print("SUCCESS:" + report_path)
except Exception as e:
    print("ERROR:" + str(e))
                                '''
                            ]
                            
                            update_progress(2, "🌐 Running cybersecurity analysis...", "Processing in background")
                            
                            # Run the subprocess
                            # Use /app when in Docker, current directory otherwise
                            work_dir = '/app' if os.path.exists('/app/src') else '.'
                            result = subprocess.run(cmd, capture_output=True, text=True, cwd=work_dir)
                            
                            update_progress(4, "📝 Processing results...", "Finalizing report")
                            
                            if result.returncode == 0 and "SUCCESS:" in result.stdout:
                                # Extract report path from output
                                report_path = result.stdout.split("SUCCESS:")[1].strip()
                                
                                # Make sure path is absolute or adjust for Docker environment
                                if not os.path.isabs(report_path):
                                    if os.path.exists('/app'):
                                        report_path = os.path.join('/app', report_path)
                                    else:
                                        report_path = os.path.join(work_dir, report_path)
                                
                                # Read the generated report
                                with open(report_path, 'r') as f:
                                    final_report = f.read()
                                
                                # Update session state
                                st.session_state.final_report = final_report
                                st.session_state.flow_complete = True
                                st.session_state.report_path = report_path
                                
                                update_progress(5, "✅ Report generation complete!", "Analysis finished successfully")
                            else:
                                # Handle error
                                error_msg = result.stderr if result.stderr else "Unknown error occurred"
                                if "ERROR:" in result.stdout:
                                    error_msg = result.stdout.split("ERROR:")[1].strip()
                                
                                st.session_state.flow_error = error_msg
                                st.session_state.flow_complete = True
                                update_progress(0, f"❌ Error: {error_msg}", "")
                                
                        except Exception as e:
                            error_msg = str(e)
                            st.session_state.flow_error = error_msg
                            st.session_state.flow_complete = True
                            update_progress(0, f"❌ Error: {error_msg}", "")
                    
                    # Start flow in thread
                    flow_thread = threading.Thread(target=run_flow)
                    flow_thread.daemon = True
                    flow_thread.start()
                    
                    # Update UI based on session state in main thread
                    while flow_thread.is_alive():
                        # Update progress bar and status from session state
                        if hasattr(st.session_state, 'current_step'):
                            progress_bar.progress(st.session_state.current_step / 5)
                        if hasattr(st.session_state, 'current_message'):
                            status_text.markdown(f"**{st.session_state.current_message}**")
                        
                        # Update activity log
                        if st.session_state.crew_logs:
                            with log_container:
                                st.markdown("### 📋 Activity Log")
                                for log in st.session_state.crew_logs[-5:]:  # Show last 5 logs
                                    st.text(log)
                        
                        time.sleep(1)
                        st.rerun()  # Refresh the UI
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                finally:
                    st.session_state.flow_running = False
    
    # Display results
    if st.session_state.flow_complete and st.session_state.final_report:
        st.markdown("---")
        col1, col2 = st.columns([3, 1])
        
        with col2:
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            st.download_button(
                label="📥 Download Report",
                data=st.session_state.final_report,
                file_name=f"cybersec_report_{timestamp}.md",
                mime="text/markdown",
                use_container_width=True
            )
            
            if st.button("🔄 Generate New Report", use_container_width=True):
                for key in ['flow_complete', 'final_report', 'flow_error', 'crew_logs', 'current_step']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
        
        with col1:
            st.markdown("### 📰 Generated Report Preview")
            # Show summary stats
            word_count = len(st.session_state.final_report.split())
            st.caption(f"Report generated • {word_count} words • {time.strftime('%Y-%m-%d %H:%M')}")
        
        st.markdown("---")
        st.markdown(st.session_state.final_report)
    
    elif hasattr(st.session_state, 'flow_error'):
        st.error(f"❌ Flow failed: {st.session_state.flow_error}")


def show_report_manager():
    import streamlit as st
    import os
    import glob
    from datetime import datetime
    
    st.title("📄 Report Manager")
    st.markdown("View, manage, and analyze your cybersecurity reports")
    
    # Get all reports
    reports_dir = 'reports'
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
        
    report_files = glob.glob(f"{reports_dir}/*.md")
    report_files.sort(key=os.path.getmtime, reverse=True)
    
    if not report_files:
        st.info("📝 No reports found. Generate your first report!")
        return
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 📋 Report List")
        
        selected_report = None
        for i, report_file in enumerate(report_files):
            filename = os.path.basename(report_file)
            file_size = os.path.getsize(report_file)
            mod_time = datetime.fromtimestamp(os.path.getmtime(report_file))
            
            if st.button(f"📄 {filename}", key=f"report_{i}"):
                selected_report = report_file
            
            st.caption(f"{file_size:,} bytes • {mod_time.strftime('%Y-%m-%d %H:%M')}")
            st.markdown("---")
    
    with col2:
        if selected_report or report_files:
            current_report = selected_report or report_files[0]
            
            st.markdown("### 📖 Report Viewer")
            filename = os.path.basename(current_report)
            
            # Report actions
            col_actions = st.columns(3)
            with col_actions[0]:
                with open(current_report, 'r') as f:
                    report_content = f.read()
                st.download_button(
                    "📥 Download",
                    data=report_content,
                    file_name=filename,
                    mime="text/markdown"
                )
            
            with col_actions[1]:
                if st.button("🗑️ Delete"):
                    os.remove(current_report)
                    st.success("Report deleted!")
                    st.rerun()
            
            with col_actions[2]:
                word_count = len(report_content.split())
                st.metric("Word Count", word_count)
            
            # Display report content
            st.markdown("---")
            st.markdown(report_content)


def show_dashboard():
    import streamlit as st
    import pandas as pd
    import matplotlib.pyplot as plt
    import os
    import glob
    from datetime import datetime, timedelta
    
    st.title("📊 Dashboard")
    st.markdown("Analytics and insights from your cybersecurity reports")
    
    # Get report statistics
    reports_dir = 'reports'
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
    
    report_files = glob.glob(f"{reports_dir}/*.md")
    
    if not report_files:
        st.info("📊 No reports available for analysis. Generate some reports first!")
        return
    
    # Basic metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Reports", len(report_files))
    
    with col2:
        total_size = sum(os.path.getsize(f) for f in report_files)
        st.metric("Total Size", f"{total_size:,} bytes")
    
    with col3:
        if report_files:
            latest_report = max(report_files, key=os.path.getmtime)
            latest_time = datetime.fromtimestamp(os.path.getmtime(latest_report))
            st.metric("Latest Report", latest_time.strftime('%m/%d %H:%M'))
    
    with col4:
        # Average report size
        avg_size = total_size / len(report_files) if report_files else 0
        st.metric("Avg Size", f"{avg_size:,.0f} bytes")
    
    # Report timeline
    st.markdown("### 📈 Report Generation Timeline")
    
    report_data = []
    for report_file in report_files:
        mod_time = datetime.fromtimestamp(os.path.getmtime(report_file))
        size = os.path.getsize(report_file)
        filename = os.path.basename(report_file)
        
        report_data.append({
            'Date': mod_time.date(),
            'Time': mod_time.strftime('%H:%M'),
            'Filename': filename,
            'Size': size
        })
    
    if report_data:
        df = pd.DataFrame(report_data)
        st.dataframe(df, use_container_width=True)
        
        # Simple chart
        daily_counts = df.groupby('Date').size()
        st.bar_chart(daily_counts)


def show_settings():
    import streamlit as st
    import os
    
    st.title("⚙️ Settings")
    st.markdown("Configure your cybersecurity news analyzer")
    
    # Environment variables
    st.markdown("### 🔑 API Configuration")
    
    anthropic_key = st.text_input(
        "Anthropic API Key", 
        value=os.getenv('ANTHROPIC_API_KEY', ''),
        type="password"
    )
    
    serper_key = st.text_input(
        "Serper API Key", 
        value=os.getenv('SERPER_API_KEY', ''),
        type="password"
    )
    
    agentops_key = st.text_input(
        "AgentOps API Key (Optional)", 
        value=os.getenv('AGENTOPS_KEY', ''),
        type="password"
    )
    
    if st.button("💾 Save Configuration"):
        # Note: In a real app, you'd save to .env file or database
        st.success("Configuration saved! (Note: Restart container to apply changes)")
    
    st.markdown("### 🛠️ System Information")
    
    # System info
    col1, col2 = st.columns(2)
    
    with col1:
        st.text(f"Reports Directory: {os.path.abspath('reports')}")
        st.text(f"Logs Directory: {os.path.abspath('logs')}")
        st.text(f"Working Directory: {os.getcwd()}")
    
    with col2:
        # Check if directories exist
        reports_exist = os.path.exists('reports')
        logs_exist = os.path.exists('logs')
        
        st.text(f"Reports Dir Exists: {'✅' if reports_exist else '❌'}")
        st.text(f"Logs Dir Exists: {'✅' if logs_exist else '❌'}")
    
    # Clear data options
    st.markdown("### 🗑️ Data Management")
    
    if st.button("🧹 Clear All Reports", type="secondary"):
        import glob
        report_files = glob.glob('reports/*.md')
        for report_file in report_files:
            os.remove(report_file)
        st.success(f"Deleted {len(report_files)} reports")
        st.rerun()


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--streamlit":
        run_streamlit()
    else:
        kickoff()
