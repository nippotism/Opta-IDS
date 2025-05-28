# Use a slim, smaller image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (for pip + gunicorn + ML libs)
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Use waitress for serving Flask
EXPOSE 5001
CMD ["waitress-serve", "--port=5001", "app:app"]