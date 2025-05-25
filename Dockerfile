# Base image
FROM ubuntu:22.04

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# Install essential packages and Python
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    python3-dev \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-setuptools \
    python3-venv \
    git \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create a symbolic link for python
RUN ln -sf /usr/bin/python3.10 /usr/bin/python

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

# Copy the application code
COPY . .

# Expose the port Flask runs on
EXPOSE 5000

# Set environment variables for Flask
ENV FLASK_APP=app/app.py
ENV FLASK_ENV=production
ENV FLASK_DEBUG=0

# Run the application with host=0.0.0.0 to allow external connections
CMD ["python", "-c", "from app.app import app; app.run(host='0.0.0.0', port=5000)"]