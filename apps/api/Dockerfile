FROM python:3.12-slim

WORKDIR /app

ENV PYTHONPATH=/app/src

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY scripts ./scripts

CMD ["uvicorn", "corebank_api.main:app", "--host", "0.0.0.0", "--port", "8000", "--app-dir", "src"]
