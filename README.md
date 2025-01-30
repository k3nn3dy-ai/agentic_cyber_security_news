# 🛡️ AI-Powered Cybersecurity News Analyzer

![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![CrewAI](https://img.shields.io/badge/CrewAI-0.86.0-orange)

An intelligent cybersecurity news aggregation and analysis system powered by AI agents that work together to gather, analyze, and report on the latest cybersecurity threats, vulnerabilities, and trends.

## 🌟 Key Features

- 🤖 **Multi-Agent System**: Leverages CrewAI to coordinate specialized AI agents:
  - Web Research Agent
  - Report Writer Agent
  - Editorial Review Agent

- 🔍 **Comprehensive Coverage**:
  - Data breaches and incidents
  - CVE vulnerabilities and zero-day exploits
  - Malware and ransomware threats
  - APT group activities
  - Industry trends
  - Regulatory changes

- 📊 **Intelligent Analysis**:
  - Severity assessment (Critical/High/Medium/Low)
  - Impact scope evaluation
  - Technical complexity rating
  - Public relevance scoring

- 📝 **Professional Reporting**:
  - Executive summaries
  - Detailed technical analysis
  - Actionable recommendations
  - Source verification
  - Editorial review process

## 🚀 Quick Start

### Prerequisites
```
Python >= 3.10, <= 3.13
uv
crewai
```

### Installation

1. Set up venv of your choice.

e.g with venv
```
python3.12 -m venv cybernews
source cybernews/bin/activate
```
3. Clone the repository:
```
git clone https://github.com/yourusername/cyber_security_news.git
cd cyber_security_news
```
2. Install dependencies:

Install UV
```
pip install uv
```
Install Crewai packages
```
pip install crewai
```
3. Setup Environment Variables
```
export OPENAI-API-KEY=="your_serper_api_key"
export SERPER_API_KEY="your_serper_api_key"
export ANTHROPIC_API_KEY"your_anthropic_key"
```
You can get a free serper api key by signing up here. https://serper.dev/

AS IS it is currently set up to run with anthropic models (Haiku and Claude Sonnet) but this can be amended to suit your preference. please find the llm guide for crewai here. https://docs.crewai.com/concepts/llms#setting-up-your-llm

4. Install cyber_security_news
```
crewai install
```
### Usage

Run the cyber news tool by using the following command:
```
crewai flow kickoff
```


## 🔧 Architecture

The system operates using three specialized crews:

1. **Web Research Crew** 🌐
   - Gathers news from trusted sources
   - Filters and ranks stories
   - Generates initial summaries

2. **Newsroom Crew** 📰
   - Synthesizes research findings
   - Creates comprehensive reports
   - Ensures proper source attribution

3. **Editorial Crew** ✍️
   - Reviews technical accuracy
   - Verifies source credibility
   - Provides quality assurance

## 📊 Output Example

The system generates a comprehensive cybersecurity report including:

- Executive Summary
- Methodology Overview
- Top News Stories
- Weekly Summary
- High-Priority Stories
- Strategic Recommendations
- Source Attribution

## 🛠️ Tools and Technologies

- CrewAI Framework
- LangChain Community Tools
- Google Serper API
- NVD CVE API Integration
- Matplotlib Visualization
- Pydantic Data Validation

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🙏 Acknowledgments

- CrewAI Team for the excellent framework
- National Vulnerability Database (NVD) for CVE data
- All contributors and security researchers

---

<p align="center">
Made with ❤️ for the cybersecurity community
</p>




