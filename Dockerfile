FROM python:3.11-slim AS base

LABEL org.opencontainers.image.authors="lexty"
LABEL org.opencontainers.image.description="GitHub Action for rendering Jinja2 templates"
LABEL org.opencontainers.image.licenses="MIT"

WORKDIR /app

# Set up dependencies
RUN pip install --no-cache-dir jinja2 pyyaml python-dotenv

# Create a builder image for multi-arch
FROM base AS builder-amd64
FROM base AS builder-arm64

# Create the final multi-architecture image
FROM builder-${TARGETARCH}

COPY entrypoint.py /app/
COPY LICENSE README.md /app/

RUN chmod +x /app/entrypoint.py

ENTRYPOINT ["/app/entrypoint.py"]