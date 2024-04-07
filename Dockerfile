FROM python:3.11.9-slim-bullseye

WORKDIR /app

COPY bot requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-m", "bot"]