# METEORICA Dockerfile
# Multi-stage build for meteorite classification framework

# ------------------------------
# Stage 1: Builder
# ------------------------------
FROM python:3.10-slim as builder

WORKDIR /build

# Install system build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
COPY pyproject.toml .
COPY setup.cfg .

# Create wheel files
RUN pip wheel --no-cache-dir --wheel-dir /build/wheels -r requirements.txt

# ------------------------------
# Stage 2: Runtime
# ------------------------------
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    DEBIAN_FRONTEND=noninteractive \
    TZ=UTC \
    METEORICA_HOME=/opt/meteorica \
    METEORICA_CONFIG=/etc/meteorica/config.yaml \
    METEORICA_DATA=/var/lib/meteorica/data

# Create meteorica user
RUN groupadd -r meteorica && useradd -r -g meteorica -m -d /opt/meteorica meteorica

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy wheels from builder
COPY --from=builder /build/wheels /wheels

# Install METEORICA and dependencies
RUN pip install --no-cache-dir --no-index --find-links=/wheels -r /wheels/requirements.txt \
    && rm -rf /wheels

# Copy application code
COPY . /opt/meteorica/src
WORKDIR /opt/meteorica/src

# Install METEORICA package
RUN pip install -e . \
    && pip install ".[dashboard]" ".[docs]"

# Create necessary directories
RUN mkdir -p $METEORICA_DATA /etc/meteorica \
    && chown -R meteorica:meteorica /opt/meteorica /var/lib/meteorica /etc/meteorica

# Copy default configuration
COPY configs/default.yaml /etc/meteorica/config.default.yaml

# Create entrypoint script
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
# Copy default config if not exists\n\
if [ ! -f "$METEORICA_CONFIG" ]; then\n\
    cp /etc/meteorica/config.default.yaml "$METEORICA_CONFIG"\n\
fi\n\
\n\
# Execute command\n\
exec "$@"\n\
' > /entrypoint.sh && chmod +x /entrypoint.sh

# Expose ports (for dashboard)
EXPOSE 8000 8501

# Set user
USER meteorica

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Default command
CMD ["meteorica", "--help"]

# ------------------------------
# Labels
# ------------------------------
LABEL org.opencontainers.image.title="METEORICA"
LABEL org.opencontainers.image.description="Celestial Messengers: Physico-Chemical Framework for Extraterrestrial Materials"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.url="https://meteorica-science.netlify.app"
LABEL org.opencontainers.image.source="https://gitlab.com/gitdeeper07/meteorica"
LABEL org.opencontainers.image.documentation="https://meteorica-science.netlify.app/documentation"
LABEL org.opencontainers.image.authors="Samir Baladi <gitdeeper@gmail.com>"
LABEL org.opencontainers.image.created="2026-02-20"
LABEL org.opencontainers.image.doi="10.14293/METEORICA.2026.001"
