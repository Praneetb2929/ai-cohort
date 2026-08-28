# Stage 1: Builder
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends build-essential

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

COPY . .

# Stage 2: Final Slim Image
FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /root/.local /root/.local
COPY --from=builder /app /app

ENV PATH=/root/.local/bin:$PATH

EXPOSE 8000 8501

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "coverage-chatbot-api.main:app", "--host", "0.0.0.0", "--port", "8000"]