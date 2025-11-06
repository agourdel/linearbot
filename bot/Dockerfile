FROM python:3.12-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
ENV LINEARBOT_CONFIG_PATH=/app/config.json
CMD ["python", "bot.py"]
