FROM python:3.14-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1

RUN groupadd -r appgroup && useradd -r -g appgroup appuser

WORKDIR /app

COPY services/extraction-service/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY services/extraction-service/main.py ./
COPY shared ./shared

RUN chown -R appuser:appgroup /app
USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]