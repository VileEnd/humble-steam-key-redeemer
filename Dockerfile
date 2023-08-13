# Use an official Python runtime as a base image
FROM python:3.9-slim

LABEL authors="Jan"

WORKDIR /app

# Install required packages and nginx
RUN apt-get update \
    && apt-get install -y nginx \
    && pip install --no-cache-dir Flask flask_socketio eventlet gunicorn

# Copy the current directory contents into the container at /app
COPY . /app

# Copy Nginx config
COPY nginx_config /etc/nginx/sites-available/default

# Expose ports
EXPOSE 80
EXPOSE 443

# Start Nginx & Gunicorn
CMD ["bash", "-c", "nginx & gunicorn -w 4 -k eventlet filterstuff:app -b 0.0.0.0:5000"]
