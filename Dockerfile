# Dockerfile
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN ln -sf /bin/bash /bin/sh

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Run collectstatic
RUN python manage.py collectstatic --noinput

# Remove .env file after collectstatic
RUN rm /app/.env

# Expose port 8000 for Django (if needed)
EXPOSE 8000

# Default command to start the application
CMD ["sh", "-c", "DJANGO_SETTINGS_MODULE=ProwlerAnalysis.settings daphne -b 0.0.0.0 -p 8000 ProwlerAnalysis.asgi:application"]
