FROM python:3.10-slim-bullseye

# Setup container
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config && \
    apt-get clean && \
    pip install --no-cache-dir --upgrade pip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /auth_service

# Copy requirements.txt first to leverage Docker cache
COPY ./requirements.txt /auth_service/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

EXPOSE 8000

# Specify the command to run
CMD ["uvicorn", "auth_service:app", "--host", "0.0.0.0", "--port", "8000"]

