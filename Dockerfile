# Use an ARM-Based Python Image
FROM python:3.9-slim-buster

LABEL authors="VileEnd"

WORKDIR /app

# Update pip first
RUN pip install --upgrade pip

# Install system-level dependencies, including cmake
RUN apt-get update && apt-get install -y \
    nginx git gcc g++ build-essential firefox-esr cmake && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Clone the repository
RUN git clone --depth 1 https://github.com/VileEnd/humble-steam-key-redeemer.git /app

# Install Python packages
RUN pip install --no-cache-dir -r /app/requirements.txt gunicorn eventlet

# Copy Nginx config
COPY nginx_config /etc/nginx/sites-available/default

# Expose ports
EXPOSE 80
EXPOSE 443

# Start Nginx & Gunicorn
CMD ["bash", "-c", "nginx & gunicorn -w 4 -k eventlet filterstuff:app -b 0.0.0.0:5000"]
