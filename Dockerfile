FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    python3-tk \
    # xvfb \
    # x11-apps \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# ENV DISPLAY=host.docker.internal:0.0
# CMD ["xvfb-run", "python", "app.main"]
CMD ["python", "-m", "app.main"]
# CMD не нужен, так как команда указана в docker-compose.yaml