FROM python:3.12-slim

# Install time utility for CPU/memory measurement
RUN apt-get update && \
    apt-get install -y --no-install-recommends time && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

# Create a non-root user for security
RUN useradd -m -s /bin/bash runner

# Set working directory
WORKDIR /app

RUN chown -R runner:runner /app

USER runner

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

CMD ["python"]