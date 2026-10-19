# Use official Python image as base
FROM python:3.12-alpine

# Set work directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip3 install --trusted-host files.pythonhosted.org --trusted-host pypi.org --trusted-host pypi.python.org -r requirements.txt

# Copy source code
COPY src/ ./src/

# Set environment variable for Telegram token (to be provided at runtime)
ENV TELEGRAM_TOKEN=""

# Declare a volume for persistent/shared data
VOLUME ["/app/data"]

# Set the entrypoint to run the bot (adjust if main entrypoint changes)
CMD ["python3", "src"]
