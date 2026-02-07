FROM python:3.11-slim

# Do not write .pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system deps required to build some Python packages if needed
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libffi-dev build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first to leverage Docker layer caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create a non-root user and give ownership of the app directory
RUN useradd --create-home appuser && chown -R appuser /app
USER appuser

# Defaults for running the webhook server
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the default webhook port (can be overridden at runtime)
EXPOSE 5000

# Run the main application
CMD ["python", "main.py"]
