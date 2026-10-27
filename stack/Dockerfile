FROM python:3.12-slim
RUN pip install --no-cache-dir prometheus-client
COPY poller.py /app/poller.py
CMD ["python", "/app/poller.py"]
