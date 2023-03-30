# # First stage: install Node.js and npm
# FROM node:16.14.0 as builder

# WORKDIR /app

# # Install bun in a custom directory
# ENV BUN_INSTALL_DIR /home/admin/.bun
# RUN mkdir -p $BUN_INSTALL_DIR
# RUN curl -fsSL https://bun.sh/install | BUN_INSTALL_DIR=$BUN_INSTALL_DIR bash

# # Second stage: create final Python image and copy dependencies
# FROM python:3.10-slim

# # Set working directory
# WORKDIR /app

# # Copy application code
# COPY . .

# # Install pip requirements as non-root user
# RUN addgroup --system appgroup && \
#     adduser --system --ingroup appgroup admin && \
#     pip install --upgrade pip && \
#     pip install --no-cache-dir -r requirements.txt && \
#     chown -R admin:appgroup /app && \
#     chown -R admin:appgroup .web && \
#     chmod -R g+w /app

# # Copy Node.js and bun from builder stage
# COPY --from=builder /usr/local/bin/node /usr/local/bin/
# COPY --from=builder --chown=admin:appgroup $BUN_INSTALL_DIR $BUN_INSTALL_DIR

# # Switch to non-root user
# USER admin

# # Expose port for application
# EXPOSE 8080

# # Start app
# CMD ["pc", "run"]


FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy application code
COPY . .

# Install pip requirements as non-root user
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup admin && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    chown -R admin:appgroup /app && \
    chmod -R g+w /app

# Switch to non-root user
USER admin

# Expose port for application
EXPOSE 8080

# Start app
CMD ["python", "ui.py"]