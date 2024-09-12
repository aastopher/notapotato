FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install pip requirements as non-root user
COPY requirements.txt .
RUN apt-get update && \
    apt-get install -y iputils-ping curl && \
    addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ .

# Permissions for non-root user
RUN chown -R appuser:appgroup /app && \
    chmod -R g+w /app

# Switch to non-root user
USER appuser

# Expose port for Nginx
EXPOSE 80

# Start app
CMD ["python", "main.py"]
