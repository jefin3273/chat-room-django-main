# Use an official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /chat-room-django-main

# Install system dependencies (including libxml2 and libxslt for lxml)
RUN apt-get update && apt-get install -y \
    libxml2-dev \
    libxslt-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy application code to the working directory
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Collect static files (optional if your app uses static files)
RUN python manage.py collectstatic --noinput

# Expose the port your app runs on
EXPOSE 8000

# Start the
