# PALMA Installation Guide

This guide covers installation of the PALMA oasis monitoring framework.

## Table of Contents
- [System Requirements](#system-requirements)
- [Quick Installation](#quick-installation)
- [Detailed Installation](#detailed-installation)
  - [1. Python Environment](#1-python-environment)
  - [2. Install PALMA](#2-install-palma)
  - [3. Database Setup](#3-database-setup)
  - [4. Configuration](#4-configuration)
  - [5. Verify Installation](#5-verify-installation)
- [Platform-Specific Instructions](#platform-specific-instructions)
  - [Linux / Ubuntu](#linux--ubuntu)
  - [macOS](#macos)
  - [Windows](#windows)
  - [Termux (Android)](#termux-android)
- [Docker Installation](#docker-installation)
- [Development Installation](#development-installation)
- [Troubleshooting](#troubleshooting)

## System Requirements

### Minimum Requirements
- **Python**: 3.10 or higher
- **RAM**: 8 GB (16 GB recommended for full satellite processing)
- **Storage**: 10 GB free space (for satellite data cache)
- **Database**: PostgreSQL 14+ with TimescaleDB extension
- **GIS**: GDAL 3.4+ (for raster processing)

### Optional Requirements
- **GPU**: CUDA-capable (for ML acceleration)
- **Internet**: For satellite data download (Sentinel-2, MODIS)
- **Sensors**: For field deployment (piezometers, EC sensors, thermocouples)

## Quick Installation

```bash
# Install from PyPI
pip install palma-oasis

# Verify installation
python -m palma --version
python -m palma doctor  # Check system compatibility
```

Detailed Installation

1. Python Environment

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Upgrade pip
pip install --upgrade pip setuptools wheel
```

2. Install PALMA

```bash
# Basic installation
pip install palma-oasis

# With all optional dependencies
pip install "palma-oasis[all]"

# Or specific extras
pip install "palma-oasis[dashboard]"  # For dashboard only
pip install "palma-oasis[pipeline]"   # For data pipeline
pip install "palma-oasis[docs]"       # For documentation
pip install "palma-oasis[dev]"        # For development
```

3. Database Setup

Install PostgreSQL with TimescaleDB

Ubuntu/Debian:

```bash
# Add PostgreSQL repository
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

# Install PostgreSQL 14
sudo apt update
sudo apt install postgresql-14 postgresql-client-14

# Add TimescaleDB repository
sudo add-apt-repository ppa:timescale/timescaledb
sudo apt update
sudo apt install timescaledb-2-postgresql-14

# Tune database
sudo timescaledb-tune --quiet --yes
sudo systemctl restart postgresql
```

macOS:

```bash
brew install postgresql@14
brew install timescaledb
timescaledb-tune
brew services start postgresql@14
```

Windows:

· Download PostgreSQL from postgresql.org
· Download TimescaleDB from timescale.com

Create Database

```bash
# Create database user
sudo -u postgres createuser --interactive --pwprompt
# Enter name: palma_user
# Enter password: [your_password]
# Superuser? n

# Create database
sudo -u postgres createdb -O palma_user palma_db

# Enable TimescaleDB
sudo -u postgres psql -d palma_db -c "CREATE EXTENSION IF NOT EXISTS timescaledb;"

# Test connection
psql -U palma_user -d palma_db -h localhost -c "\dx"
```

4. Configuration

```bash
# Create configuration directory
mkdir -p ~/.palma
mkdir -p ~/.palma/sites
mkdir -p ~/.palma/data
mkdir -p ~/.palma/logs

# Copy default configuration
cp config/palma.default.yaml ~/.palma/config.yaml

# Edit configuration
nano ~/.palma/config.yaml
# Set database credentials, API keys, etc.

# Set environment variable
export PALMA_CONFIG=~/.palma/config.yaml
# Add to .bashrc or .zshrc for persistence
```

5. Verify Installation

```bash
# Run diagnostics
python -m palma doctor

# Expected output:
# ✓ Python 3.10+ detected
# ✓ PostgreSQL 14+ with TimescaleDB
# ✓ GDAL 3.4+ available
# ✓ Dependencies installed
# ✓ Configuration file found
# ✓ Database connection successful

# Run tests
python -m pytest --pyargs palma -v

# Test with sample data
python -m palma demo --site draa_valley
```

Platform-Specific Instructions

Linux / Ubuntu

Install system dependencies:

```bash
sudo apt update
sudo apt install -y \
    python3.10 python3.10-dev python3.10-venv \
    postgresql-14 postgresql-client-14 \
    libgdal-dev gdal-bin \
    libnetcdf-dev libhdf5-dev \
    libgeos-dev libproj-dev \
    cmake build-essential
```

macOS

Install system dependencies:

```bash
# Install Homebrew if not present
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install packages
brew install python@3.10
brew install postgresql@14
brew install timescaledb
brew install gdal
brew install netcdf
brew install hdf5
brew install geos
brew install proj
```

Windows

Using WSL2 (Recommended):

```bash
# In PowerShell as Administrator
wsl --install -d Ubuntu

# Then follow Linux instructions inside WSL
```

Native Windows:

```bash
# Download Python 3.10 from python.org
# Download PostgreSQL from postgresql.org
# Download OSGeo4W for GDAL (gdal.org)

# Use PowerShell
python -m venv .venv
.venv\Scripts\activate
pip install palma-oasis
```

Termux (Android)

```bash
# Update packages
pkg update && pkg upgrade

# Install dependencies
pkg install python python-pip
pkg install postgresql
pkg install gdal
pkg install libgeos
pkg install proj
pkg install cmake

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install PALMA
pip install palma-oasis

# Note: TimescaleDB requires additional setup on Termux
# Consider using SQLite for mobile deployments
```

Docker Installation

Using pre-built image

```bash
# Pull image
docker pull gitlab.com/gitdeeper4/palma:latest

# Run container
docker run -d \
  --name palma \
  -p 8000:8000 \
  -p 8501:8501 \
  -v ~/.palma:/root/.palma \
  -e PALMA_CONFIG=/root/.palma/config.yaml \
  gitlab.com/gitdeeper4/palma:latest
```

Docker Compose (full stack)

```bash
# Clone repository
git clone https://gitlab.com/gitdeeper4/palma.git
cd palma

# Start all services
docker-compose up -d

# Services:
# - PostgreSQL:5432
# - Redis:6379
# - API:8000
# - Dashboard:8501
# - Celery workers
# - Flower (monitoring):5555

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Development Installation

For contributors and developers:

```bash
# Clone repository
git clone https://gitlab.com/gitdeeper4/palma.git
cd palma

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install in development mode with all extras
pip install -e ".[all]"

# Install pre-commit hooks
pre-commit install

# Set up test database
createdb palma_test
psql palma_test -c "CREATE EXTENSION timescaledb;"

# Run tests
pytest tests/ -v --cov=palma
```

Troubleshooting

Common Issues

GDAL not found

```bash
# Ubuntu
sudo apt install libgdal-dev gdal-bin

# macOS
brew install gdal

# Set environment variables if needed
export CPLUS_INCLUDE_PATH=/usr/include/gdal
export C_INCLUDE_PATH=/usr/include/gdal
```

Database connection failed

```bash
# Check PostgreSQL is running
sudo systemctl status postgresql  # Linux
brew services list | grep postgres  # macOS

# Test connection
psql -U palma_user -d palma_db -h localhost

# Update pg_hba.conf if needed
# Add: host all all 127.0.0.1/32 md5
```

Memory issues

```bash
# Reduce parallel processing
export PALMA_MAX_WORKERS=2

# Use chunked processing
python -m palma pipeline run --chunk-size 1000
```

Satellite data download fails

```bash
# Check internet connection
ping copernicus.eu

# Update API credentials
# Edit ~/.palma/config.yaml
# Add Sentinel Hub credentials

# Use alternative source
# Set: provider: "aws_s3" in config
```

Getting Help

· Documentation: https://palma-oasis.readthedocs.io
· Issues: https://gitlab.com/gitdeeper4/palma/-/issues
· Discussions: https://gitlab.com/gitdeeper4/palma/-/discussions
· Email: palma-dev@googlegroups.com

Verify Installation Script

```bash
# Create verification script
cat > verify_palma.py << 'EOF'
#!/usr/bin/env python
"""PALMA installation verification script."""

import sys
import importlib

def check_module(module_name):
    try:
        importlib.import_module(module_name)
        print(f"✓ {module_name}")
        return True
    except ImportError as e:
        print(f"✗ {module_name}: {e}")
        return False

def main():
    print("PALMA Installation Verification")
    print("=" * 40)
    
    # Check Python version
    print(f"Python: {sys.version[:5]}")
    
    # Check core modules
    modules = [
        "palma",
        "palma.parameters",
        "palma.ohi",
        "palma.hydrology",
        "palma.thermal",
        "palma.salinity",
        "palma.remote_sensing",
        "palma.biodiversity",
        "palma.io",
        "palma.validation",
        "palma.alerts",
        "palma.utils"
    ]
    
    success = True
    for module in modules:
        if not check_module(module):
            success = False
    
    # Check version
    try:
        from palma import __version__
        print(f"PALMA version: {__version__}")
    except:
        print("✗ Could not determine version")
        success = False
    
    if success:
        print("\n✅ PALMA installation successful!")
    else:
        print("\n❌ PALMA installation has issues")
        sys.exit(1)

if __name__ == "__main__":
    main()
