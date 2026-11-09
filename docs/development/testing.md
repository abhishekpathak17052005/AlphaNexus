# ALPHANEXUS – Testing Guide

## 1. Running the Test Suite

```bash
# Run all unit tests
PYTHONPATH=backend pytest tests/unit/ -v

# Run API and integration tests
PYTHONPATH=backend pytest tests/integration/ -v

# Run full end-to-end workflow tests
PYTHONPATH=backend pytest tests/e2e/ -v

# Run entire test suite
PYTHONPATH=backend pytest tests/ -v
```
