# Use the official Python image as base
FROM python:3.10-slim
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Expose the port the app runs on
EXPOSE 8010

# Command to run the application
CMD ["python", "-m", "flask", "run", "-p", "8010", "-h", "0.0.0.0"]
