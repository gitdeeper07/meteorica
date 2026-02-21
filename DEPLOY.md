# PALMA Deployment Guide

This guide covers deployment options for the PALMA oasis monitoring system.

## Table of Contents
- [Quick Deployments](#quick-deployments)
  - [Netlify (Dashboard)](#netlify-dashboard)
  - [Hugging Face Spaces (Interactive)](#hugging-face-spaces-interactive)
  - [PyPI (Python Package)](#pypi-python-package)
  - [ReadTheDocs (Documentation)](#readthedocs-documentation)
- [Production Deployments](#production-deployments)
  - [Docker Compose](#docker-compose)
  - [Kubernetes](#kubernetes)
  - [Cloud Providers](#cloud-providers)
- [Database Setup](#database-setup)
- [Monitoring Pipeline](#monitoring-pipeline)
- [Configuration](#configuration)
- [Security](#security)
- [Backup & Recovery](#backup--recovery)
- [Scaling](#scaling)

## Quick Deployments

### Netlify (Dashboard)

The PALMA dashboard is pre-configured for Netlify deployment.

#### Automatic Deployment

1. Connect your Git repository to Netlify
2. Use these settings:
   - Build command: `npm run build` (if using Node) or leave empty
   - Publish directory: `dashboard`
   - Environment variables: none required

3. Or use the `netlify.toml` configuration:
```toml
[build]
  publish = "dashboard"

[build.environment]
  PYTHON_VERSION = "3.11"

[redirects]
  from = "/api/*"
  to = "https://your-api-domain.com/:splat"
  status = 200
```

Manual Deployment

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
netlify deploy --prod --dir=dashboard
```

Live demo: https://palma-oasis.netlify.app

Hugging Face Spaces (Interactive)

Deploy an interactive version with Streamlit.

Using Git

```bash
# Create space at huggingface.co/new-space
# Choose Streamlit SDK

git clone https://huggingface.co/spaces/gitdeeper4/palma
cp -r dashboard/* palma-space/
cd palma-space

# Create README.md
cat > README.md << 'EOF'
---
title: PALMA Oasis Monitor
emoji: 🌴
colorFrom: green
colorTo: earth
sdk: streamlit
sdk_version: 1.28.0
app_file: app.py
pinned: false
---

# PALMA Oasis Monitoring
Real-time oasis health monitoring system.
