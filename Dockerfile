# Use an official Python runtime as a base image
FROM python:3.9-slim

LABEL authors="Jan"

WORKDIR /app

# Install required packages, nginx, and git
RUN apt-get update \
    && apt-get install -y nginx git \
    && pip install --no-cache-dir Flask flask_socketio eventlet gunicorn

# Clone the GitHub repository
RUN git clone https://github.com/VileEnd/humble-steam-key-redeemer.git /app

# Copy Nginx config (Assuming you have it in the same folder as the Dockerfile, adjust as needed)
COPY nginx_config /etc/nginx/sites-available/default

# Expose ports
EXPOSE 80
EXPOSE 443

# Start Nginx & Gunicorn
CMD ["bash", "-c", "nginx & gunicorn -w 4 -k eventlet filterstuff:app -b 0.0.0.0:5000"]
