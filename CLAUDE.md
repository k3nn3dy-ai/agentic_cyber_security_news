# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### 🐳 Docker Setup (RECOMMENDED)

**Quick Start:**
```bash
# 1. Copy environment template and add your API keys
cp example.env .env
# Edit .env with your actual API keys:
# ANTHROPIC_API_KEY=your_anthropic_key_here
# SERPER_API_KEY=your_serper_key_here

# 2. Run Streamlit web interface
docker-compose up cybersec-web

# Access at http://localhost:8501
```

**Docker Compose Commands:**
```bash
# Web interface (default)
docker-compose up cybersec-web

# CLI mode (one-time report generation)
docker-compose run cybersec-cli

# Build/rebuild image
docker-compose build

# Clean shutdown
docker-compose down

# View logs
docker-compose logs cybersec-web
```

**Manual Docker Commands:**
```bash
# Build image
docker build -t cybersec-news-ai .

# Run Streamlit interface
docker run -p 8501:8501 \
    -e ANTHROPIC_API_KEY="your_key" \
    -e SERPER_API_KEY="your_key" \
    -v $(pwd)/reports:/app/reports \
    -v $(pwd)/logs:/app/logs \
    cybersec-news-ai

# Run CLI mode
docker run \
    -e ANTHROPIC_API_KEY="your_key" \
    -e SERPER_API_KEY="your_key" \
    -v $(pwd)/reports:/app/reports \
    cybersec-news-ai \
    python -m cyber_security_news.main kickoff
```

### Local Development (Alternative)
```bash
# Install dependencies
crewai install

# Run CLI
PYTHONPATH=src python -m cyber_security_news.main kickoff

# Run Streamlit locally
cd cyber_security_news && PYTHONPATH=src streamlit run streamlit_app.py

# Plot flow diagram
PYTHONPATH=src python -m cyber_security_news.main plot
```

### Environment Variables
Required environment variables:
- `ANTHROPIC_API_KEY`: For Anthropic Claude models (Haiku and Sonnet)  
- `SERPER_API_KEY`: For Google search functionality via Serper API
- `AGENTOPS_KEY`: Optional for AgentOps monitoring (currently commented out)

Copy `example.env` to `.env` and fill in your API keys:
```bash
cp example.env .env
# Edit .env with your actual API keys
```

### Version Information
- **CrewAI**: Upgraded to v0.177.0 (from v0.86.0)
- **Python**: 3.10-3.13 supported
- **Key Dependencies**: Streamlit, OpenAI >=1.13.3, LangChain Community

## Architecture

This is a **CrewAI-based multi-agent cybersecurity news analysis system** that uses a **Flow pattern** to orchestrate three specialized crews in sequence:

### Core Flow Structure (`main.py:34-108`)
The `CyberSecurityNewsFlow` implements a state-driven flow with retry logic:

1. **Web Research Phase** - Gathers raw cybersecurity news
2. **Newsroom Phase** - Synthesizes findings into comprehensive reports  
3. **Editorial Review Phase** - Quality assurance with retry capability (max 3 attempts)
4. **Publication** - Final report generation

### Three-Crew Architecture

**1. Web Research Crew** (`web_research_crew.py`)
- **Agent**: `web_researcher` 
- **Tools**: GoogleNewsSearch, CVE data fetching
- **Tasks**: search → filter → summarize → weekly overview → CISA KEV analysis
- **Output**: Structured research data in markdown files

**2. Newsroom Crew** (`newsroom_crew.py`) 
- **Agent**: `report_writer`
- **Tools**: FileReadTool for consuming research outputs
- **Task**: Synthesize research into professional cybersecurity report
- **Output**: `weekly_cyber_security_news_report.md`

**3. Editor Crew** (`editor.py`)
- **Agent**: `newsroom_editor` 
- **Task**: Quality review with boolean acceptance decision
- **Output**: Structured feedback with `is_acceptable` flag

### Key Components

- **Custom Tools** (`tools/`): Google search, CVE checks, JSON reporting, exploitability analysis
- **Configuration**: YAML-based agent/task definitions in each crew's `config/` directory
- **State Management**: Pydantic models for flow state and crew outputs
- **Logging**: Individual log files per crew for debugging

### Project Structure
```
cyber_security_news/
├── src/cyber_security_news/
│   ├── main.py              # Flow orchestration
│   ├── crews/               # Three specialized crews
│   │   ├── web_research_crew/
│   │   ├── newsroom_crew/
│   │   └── editor/
│   └── tools/               # Custom CrewAI tools
├── streamlit_app.py         # Web interface
└── pyproject.toml          # Dependencies and scripts
```

The system is designed for **defensive cybersecurity analysis** - gathering, analyzing, and reporting on threats, vulnerabilities, and security trends from public sources.

### Streamlit Web Interface

The system includes a comprehensive web interface built with Streamlit:

**🚀 Generate Report Page:**
- Configuration options (focus areas, report depth, CVE analysis)
- Real-time progress tracking with crew activity logs
- Visual progress indicators for each crew phase
- Live status updates during generation
- Automatic report saving and preview

**📄 Report Manager:**
- View all generated reports in chronological order
- File browser with size and timestamp info
- Download, delete, and view reports
- Word count and metadata display
- Full report content viewer

**📊 Dashboard:**
- Report generation analytics and metrics
- Timeline visualization of report history
- File size and generation frequency stats
- Data trends and usage insights

**⚙️ Settings:**
- API key configuration interface
- System information and directory status
- Data management and cleanup tools
- Environment variable validation

**Access:** The multi-page Streamlit app provides a complete management interface for cybersecurity news analysis with navigation, persistent storage, and comprehensive report lifecycle management.