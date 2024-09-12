FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu --trusted-host download.pytorch.org && \
    chown -R appuser:appgroup /app && \
    chmod -R g+w /app

COPY app/ .
USER appuser
EXPOSE 8000

# start application server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker", "main:app"]