# Restful Booker API Automation

This project contains automated tests for the Restful Booker API using Python, pytest, and BDD (Behavior Driven Development) approach.

## Project Structure

```
restful_booker_automation/
├── features/                    # BDD feature files (.feature)
├── tests/                       # Test implementation
│   ├── step_definitions/        # BDD step definitions
│   ├── helpers/                 # Reusable helper classes
│   └── __init__.py
├── data/                        # Test data and payloads
├── config/                      # Configuration files
├── reports/                     # Test execution reports
├── requirements.txt             # Python dependencies
├── pytest.ini                  # Pytest configuration
├── conftest.py                  # Shared fixtures
└── README.md                    # Documentation
```

## Setup

1. Install Python 3.8 or higher
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running Tests

```bash
# Run all tests
pytest

# Run tests with specific markers
pytest -m smoke
pytest -m regression

# Generate HTML report
pytest --html=reports/report.html
```

## API Documentation

The tests are written for the Restful Booker API: https://restful-booker.herokuapp.com/apidoc/

## Features

- BDD approach using pytest-bdd
- Comprehensive API test coverage
- HTML and JSON reporting
- Configurable test execution
- Reusable helper functions and fixtures
