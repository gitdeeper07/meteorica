#!/bin/bash
# Run all METEORICA tests

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "🚀 Running METEORICA tests..."
echo "================================"

# Unit tests
echo -e "\n${GREEN}Running unit tests...${NC}"
python -m pytest tests/unit/ -v

# Integration tests
echo -e "\n${GREEN}Running integration tests...${NC}"
python -m pytest tests/integration/ -v

# Coverage report
echo -e "\n${GREEN}Generating coverage report...${NC}"
python -m pytest tests/ --cov=meteorica --cov-report=term --cov-report=html

echo -e "\n${GREEN}All tests complete!${NC}"
