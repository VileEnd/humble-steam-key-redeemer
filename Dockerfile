# Use an ARM-Based Python Image
FROM python:3.9-slim-buster

LABEL authors="Jan"

WORKDIR /app

RUN apt-get update && apt-get install -y \
    nginx git gcc g++ build-essential firefox-esr && \
    git clone --depth 1 https://github.com/VileEnd/humble-steam-key-redeemer.git /app && \
    pip install --no-cache-dir -r /app/requirements.txt gunicorn eventlet && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy Nginx config
COPY nginx_config /etc/nginx/sites-available/default

# Expose ports
EXPOSE 80
EXPOSE 443

# Start Nginx & Gunicorn
CMD ["bash", "-c", "nginx & gunicorn -w 4 -k eventlet filterstuff:app -b 0.0.0.0:5000"]
