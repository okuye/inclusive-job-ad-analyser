# Dockerfile for Inclusive Job Ad Analyzer

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY requirements.txt .
COPY setup.py .
COPY pyproject.toml .
COPY README.md .
COPY src/ src/
COPY data/ data/
COPY config/ config/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    python -m spacy download en_core_web_sm

# Expose port for Gradio
EXPOSE 7860

# Set environment variables
ENV GRADIO_SERVER_NAME="0.0.0.0"
ENV GRADIO_SERVER_PORT=7860

# Run the web application by default
CMD ["python", "-m", "inclusive_job_ad_analyser"]
