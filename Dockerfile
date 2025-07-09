# Use official Python image
FROM python:3.11-slim

WORKDIR /app

# Install build tools for netifaces and other native dependencies
RUN apt-get update && \
    apt-get remove -y avahi-daemon libnss-mdns || true && \
    apt-get install -y gcc python3-dev net-tools iproute2 iputils-ping && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose all ports (dynamic port selection)
EXPOSE 5000

CMD ["python", "droplan/backend/app.py"] 