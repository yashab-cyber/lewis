# Use an official lightweight Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Copy all project files into container
COPY . /app/

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    portaudio19-dev \
    libsndfile1 \
    espeak \
    git \
    curl \
    nmap \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port for Flask backend
EXPOSE 5000

# Start LEWIS via main.py (can be changed to flask server later)
CMD ["python", "main.py"]
