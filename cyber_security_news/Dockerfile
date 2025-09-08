# Use Python 3.12 slim image as base
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH=/app/src

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /app/

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Create a non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Set environment variables placeholder
# These should be provided at runtime
ENV AGENTOPS_KEY="" \
    SERPER_API_KEY="" \
    ANTHROPIC_API_KEY=""

# Create directories for output
RUN mkdir -p /app/reports /app/logs

# Expose port for Streamlit
EXPOSE 8501

# Default to Streamlit interface
CMD ["streamlit", "run", "streamlit_app.py", "--server.address=0.0.0.0", "--server.port=8501", "--server.headless=true"]

# Health check for Streamlit
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Labels
LABEL maintainer="Your Name <your.email@example.com>" \
      version="0.2.0" \
      description="AI-Powered Cybersecurity News Analyzer with Streamlit UI" \
      org.opencontainers.image.source="https://github.com/yourusername/cyber_security_news" 