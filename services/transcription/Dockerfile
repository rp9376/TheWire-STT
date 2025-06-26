# Transcription Service Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install ffmpeg and clean up
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
