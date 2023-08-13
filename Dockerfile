# Use an ARM-Based Python Image
FROM python:3.9-slim-buster

LABEL authors="Jan"

WORKDIR /app

# Update
RUN apt-get update

# Install build tools, Firefox, and necessary packages
RUN apt-get install -y nginx git gcc g++ build-essential firefox-esr

# Clone the GitHub repository
RUN git clone https://github.com/VileEnd/humble-steam-key-redeemer.git /app

# Copy Nginx config
COPY nginx_config /etc/nginx/sites-available/default

# Expose ports
EXPOSE 80
EXPOSE 443

# Start Nginx & Gunicorn
CMD ["bash", "-c", "nginx & gunicorn -w 4 -k eventlet filterstuff:app -b 0.0.0.0:5000"]
