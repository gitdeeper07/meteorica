# Contributing to PALMA

First off, thank you for considering contributing to PALMA! We welcome contributions from ecologists, hydrologists, remote sensing specialists, software engineers, and anyone passionate about preserving desert oasis ecosystems.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Adding New Sites](#adding-new-sites)
- [Reporting Issues](#reporting-issues)
- [Contact](#contact)

## Code of Conduct

This project adheres to a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to gitdeeper@gmail.com.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Git
- PostgreSQL 14+ with TimescaleDB
- GDAL 3.4+

### Setup Development Environment

```bash
# Fork the repository on GitLab, then clone your fork
git clone https://gitlab.com/YOUR_USERNAME/palma.git
cd palma

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
pre-commit install

# Set up database (if needed for integration tests)
createdb palma_test
psql palma_test -c "CREATE EXTENSION timescaledb;"
```

Verify Setup

```bash
pytest tests/unit/ -v
ruff check palma/
mypy palma/
```

Development Workflow

1. Create an issue describing your proposed changes (unless it's a trivial fix)
2. Discuss with maintainers to ensure alignment
3. Fork and branch:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-description
   ```
4. Make changes following our coding standards
5. Write/update tests for your changes
6. Run tests locally and ensure they pass
7. Commit with clear messages
8. Push to your fork
9. Open a Merge Request

Branch Naming

· feature/ - New features
· fix/ - Bug fixes
· docs/ - Documentation updates
· refactor/ - Code refactoring
· test/ - Test improvements
· perf/ - Performance optimizations

Pull Request Process

1. Update documentation for any changed functionality
2. Add tests for new features (coverage should not decrease)
3. Update CHANGELOG.md with your changes under "Unreleased"
4. Ensure CI passes (tests, linting, type checking)
5. Request review from maintainers
6. Address review feedback
7. Merge after approval and CI passes

PR Template

```markdown
## Description
Brief description of changes

## Related Issue
Fixes #(issue number)

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring
- [ ] Test update

## How Has This Been Tested?
Describe tests you added/ran

## Checklist
- [ ] Tests pass locally
- [ ] Docs updated
- [ ] CHANGELOG updated
- [ ] Code follows style guidelines
- [ ] Type hints added/updated
```

Coding Standards

Python

· Format: Black (line length 88)
· Imports: isort with black profile
· Linting: ruff (see pyproject.toml for rules)
· Type Hints: Required for all public functions
· Docstrings: Google style

Example

```python
"""Module description."""

from typing import Optional, Union

import numpy as np


def calculate_arvc(
    hydraulic_conductivity: float,
    head_gradient: float,
    alpha: float = 0.68,
    **kwargs
) -> float:
    """Calculate Aquifer Recharge Velocity Coefficient.
    
    Args:
        hydraulic_conductivity: Hydraulic conductivity in m/d
        head_gradient: Hydraulic head gradient (dh/dl)
        alpha: Non-linear retention exponent (default 0.68)
        **kwargs: Additional parameters
    
    Returns:
        ARVC value normalized to [0,1] scale
        
    Raises:
        ValueError: If inputs are invalid
    """
    if hydraulic_conductivity <= 0:
        raise ValueError("hydraulic_conductivity must be positive")
    
    # Implementation
    result = ...
    
    return result
```

Testing Guidelines

Test Structure

```
tests/
├── conftest.py              # Fixtures
├── unit/                    # Unit tests
│   ├── test_arvc.py
│   ├── test_ptsi.py
│   └── ...
├── integration/             # Integration tests
│   ├── test_pipeline.py
│   └── test_api.py
└── fixtures/                # Test data
    ├── sample_data.csv
    └── sample_scene.tif
```

Writing Tests

```python
import pytest
from palma.parameters import ARVC

def test_arvc_computation(sample_piezometer_data):
    """Test ARVC calculation with valid data."""
    arvc = ARVC(hydraulic_conductivity=12.4, head_gradient=0.003)
    result = arvc.compute(sample_piezometer_data)
    
    assert 0 <= result.value <= 1
    assert result.alert_level in ["EXCELLENT", "GOOD", "MODERATE", "CRITICAL", "COLLAPSE"]

@pytest.mark.parametrize("kc,gradient,expected", [
    (10.0, 0.001, 0.92),
    (5.0, 0.005, 0.78),
])
def test_arvc_expected_values(kc, gradient, expected):
    """Test ARVC with known expected values."""
    arvc = ARVC(hydraulic_conductivity=kc, head_gradient=gradient)
    result = arvc.compute(...)
    assert abs(result.value - expected) < 0.05
```

Running Tests

```bash
# All tests
pytest

# Unit tests only
pytest tests/unit/

# Integration tests
pytest tests/integration/

# With coverage
pytest --cov=palma --cov-report=html

# Specific test
pytest tests/unit/test_arvc.py::test_arvc_computation -v
```

Documentation

Building Documentation

```bash
cd docs
make html  # or make latexpdf for PDF
```

Documentation Standards

· README.md: Project overview, quick start
· docs/: Detailed documentation
· docstrings: In-code documentation
· notebooks: Example notebooks

Adding New Parameters

If adding a new monitoring parameter:

1. Create module in palma/parameters/
2. Add to palma/parameters/__init__.py
3. Update palma/ohi/composite.py
4. Add documentation in docs/parameters/
5. Add tests in tests/unit/
6. Update dashboard components

Adding New Sites

To add a new monitoring site:

1. Create site configuration in config/sites/
2. Add to palma/io/site_loader.py
3. Update site list in documentation
4. Add sample data in tests/fixtures/
5. Test with pytest tests/integration/test_site_integration.py

Site Configuration Template

```yaml
# config/sites/new_site.yaml
name: "New Oasis"
country: "Country"
coordinates:
  lat: 31.5
  lon: -5.2
elevation: 850  # meters
area_ha: 1200
type: "artesian"  # artesian, wadi, aquifer, fog

sensors:
  piezometers:
    count: 12
    depths: [15, 30, 60, 90]
  soil_ec:
    count: 24
    depths: [15, 30, 60, 90]
  thermocouples:
    count: 8
    layers: 4

parameters:
  arvc:
    alpha: 0.68
    k_sat_mean: 12.4
  sssp:
    ec_crit: 8.4
    ec_baseline: 1.2

monitoring:
  tier: 2  # 1, 2, or 3
  start_date: 2024-01-01
  frequency: "hourly"
```

Reporting Issues

Bug Reports

Include:

· Clear title and description
· Steps to reproduce
· Expected vs actual behavior
· Environment details (OS, Python version, package versions)
· Logs or screenshots

Feature Requests

Include:

· Use case description
· Expected behavior
· Potential implementation approach
· References to similar features

Contact

· Issues: GitLab Issues
· Discussions: GitLab Discussions
· Email: palma-dev@googlegroups.com
· Matrix: #palma-oasis:matrix.org

---

Thank you for contributing to PALMA! 🌴
