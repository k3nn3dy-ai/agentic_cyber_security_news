# Use Python 3.10 slim image as base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

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
    SERPER_API_KEY=""

# Create directories for output
RUN mkdir -p /app/reports /app/logs

# Set default command
ENTRYPOINT ["python", "-m", "cyber_security_news.main"]
CMD ["kickoff"]

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Labels
LABEL maintainer="Your Name <your.email@example.com>" \
      version="0.1.0" \
      description="AI-Powered Cybersecurity News Analyzer" \
      org.opencontainers.image.source="https://github.com/yourusername/cyber_security_news" 