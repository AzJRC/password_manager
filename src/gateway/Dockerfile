FROM python:3.10-slim-bullseye

# Setup container
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    net-tools \
    iputils-ping \
    default-libmysqlclient-dev \
    pkg-config && \
    apt-get clean && \
    pip install --no-cache-dir --upgrade pip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /gateway

# Copy requirements.txt first to leverage Docker cache
COPY ./requirements.txt /gateway

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /gateway

ENV AUTH_SERVICE_URL 127.0.0.1:8002
ENV VAULT_SERVICE_URL 127.0.0.1:8003

EXPOSE 8001

# Specify the command to run
CMD ["fastapi","run", "--host", "0.0.0.0", "--port", "8001", "gateway.py"]
