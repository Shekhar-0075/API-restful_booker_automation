# RESTful Booker API Test Automation Framework

A comprehensive API test automation framework for the [RESTful Booker API](https://restful-booker.herokuapp.com) built with Python, pytest, and pytest-bdd. This framework provides robust testing capabilities including functional, security, performance, and negative testing scenarios.

## 🚀 Features

- **🎯 Comprehensive Test Coverage**: Functional, security, performance, and negative testing
- **🔧 BDD Approach**: Behavior-driven development with Gherkin feature files
- **📊 Rich Reporting**: HTML and JSON reports with detailed test analytics
- **🔄 CI/CD Integration**: GitHub Actions workflow for automated testing
- **🛡️ Security Testing**: Built-in security validation and vulnerability checks
- **⚡ Performance Testing**: Response time validation and performance thresholds
- **🔀 Parallel Execution**: Support for parallel test execution with pytest-xdist
- **📈 Advanced Analytics**: Custom reporting with performance metrics
- **🎨 Modular Architecture**: Clean, maintainable code structure with helper classes
- **🔧 Configurable**: Environment-specific configurations and flexible test execution

## 📋 Table of Contents

- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Test Execution](#-test-execution)
- [CI/CD Integration](#-cicd-integration)
- [Test Categories](#-test-categories)
- [Reporting](#-reporting)
- [Contributing](#-contributing)
- [Troubleshooting](#-troubleshooting)

## 📁 Project Structure

```
restful_booker_automation/
├── 📂 config/                     # Configuration files
│   ├── config.py                  # Main configuration class
│   └── environments.json          # Environment-specific settings
├── 📂 data/                       # Test data files
│   ├── booking_data.json          # Valid booking test data
│   ├── invalid_data.json          # Invalid data for negative tests
│   └── test_schemas.json          # JSON schemas for validation
├── 📂 features/                   # BDD feature files (Gherkin)
│   ├── auth.feature               # Authentication scenarios
│   ├── booking_crud.feature       # CRUD operations
│   ├── booking_search.feature     # Search functionality
│   └── negative_tests.feature     # Negative test scenarios
├── 📂 tests/                      # Test implementation
│   ├── 📂 data/
│   │   └── booking_factory.py     # Test data factory
│   ├── 📂 helpers/                # Helper classes
│   │   ├── api_helper.py          # Core API operations
│   │   ├── auth_helper.py         # Authentication utilities
│   │   ├── booking_helper.py      # Booking-specific operations
│   │   ├── performance_helper.py  # Performance testing utilities
│   │   └── security_helper.py     # Security testing utilities
│   ├── 📂 step_definitions/       # BDD step implementations
│   │   ├── test_auth.py           # Authentication step definitions
│   │   ├── test_booking_crud.py   # CRUD step definitions
│   │   ├── test_booking_search.py # Search step definitions
│   │   └── test_negative_tests.py # Negative test implementations
│   └── 📂 utils/
│       └── advanced_reporter.py   # Custom reporting utilities
├── 📂 reports/                    # Generated test reports
├── 📂 .github/workflows/          # CI/CD workflows
│   └── api-tests.yml              # GitHub Actions workflow
├── conftest.py                    # pytest configuration and fixtures
├── pytest.ini                     # pytest settings
├── requirements.txt               # Python dependencies
├── test_runner.py                 # Interactive test runner
└── README.md                      # This file
```

## 🔧 Prerequisites

- **Python 3.12+** (recommended)
- **pip** (Python package installer)
- **Git** (for version control)
- **Internet connection** (to access RESTful Booker API)

## 📦 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd restful_booker_automation
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Verify Installation

```bash
pytest --version
python test_runner.py
```

## ⚙️ Configuration

### Environment Variables

Set the following environment variables (optional):

```bash
# API Configuration
export API_BASE_URL="https://restful-booker.herokuapp.com"
export TEST_ENV="production"
export REQUEST_TIMEOUT="30"
export RETRY_COUNT="3"
export RETRY_BACKOFF="1.5"
```

### Environment-Specific Configuration

Edit `config/environments.json` for environment-specific settings:

```json
{
  "production": {
    "base_url": "https://restful-booker.herokuapp.com",
    "timeout": 30,
    "retry_count": 3,
    "rate_limit_aware": true
  },
  "staging": {
    "base_url": "https://staging-restful-booker.herokuapp.com",
    "timeout": 45,
    "retry_count": 5,
    "rate_limit_aware": false
  }
}
```

## 🎯 Usage

### Interactive Test Runner

The easiest way to run tests is using the interactive test runner:

```bash
python test_runner.py
```

This will present a menu with the following options:

```
Available test suites:
 1. Smoke Tests
 2. Functional Tests
 3. Non-Functional Tests
 4. Positive Tests
 5. Negative Tests
 6. Auth Module Only
 7. CRUD Module Only
 8. Search Module Only
 9. All Tests
```

### Command Line Execution

You can also run tests directly with pytest:

```bash
# Run all tests
pytest -v

# Run specific test categories
pytest -m smoke -v                    # Smoke tests
pytest -m functional -v               # Functional tests
pytest -m security -v                 # Security tests
pytest -m negative -v                 # Negative tests
pytest -m positive -v                 # Positive tests

# Run specific modules
pytest tests/step_definitions/test_auth.py -v
pytest tests/step_definitions/test_booking_crud.py -v
pytest tests/step_definitions/test_booking_search.py -v

# Run with parallel execution
pytest -n auto -v                     # Auto-detect CPU cores
pytest -n 4 -v                        # Use 4 parallel workers

# Generate custom reports
pytest --html=reports/custom_report.html --self-contained-html -v
```

## 🧪 Test Execution

### Test Categories and Markers

The framework uses pytest markers to categorize tests:

| Marker        | Description                  | Usage                   |
| ------------- | ---------------------------- | ----------------------- |
| `smoke`       | Critical functionality tests | `pytest -m smoke`       |
| `functional`  | Feature testing              | `pytest -m functional`  |
| `security`    | Security validation          | `pytest -m security`    |
| `performance` | Response time validation     | `pytest -m performance` |
| `negative`    | Error condition testing      | `pytest -m negative`    |
| `positive`    | Happy path scenarios         | `pytest -m positive`    |
| `auth`        | Authentication tests         | `pytest -m auth`        |
| `booking`     | Booking operations           | `pytest -m booking`     |
| `crud`        | CRUD operations              | `pytest -m crud`        |
| `search`      | Search functionality         | `pytest -m search`      |

### Advanced Test Execution

```bash
# Run tests with specific markers combination
pytest -m "smoke and positive" -v
pytest -m "functional and not security" -v

# Run tests with custom timeout
pytest --timeout=60 -v

# Run tests with detailed output
pytest -v --tb=long --capture=no

# Run tests and stop on first failure
pytest -x -v

# Run tests with coverage
pytest --cov=tests --cov-report=html -v
```

## 🔄 CI/CD Integration

### GitHub Actions Workflow

The project includes a comprehensive GitHub Actions workflow (`.github/workflows/api-tests.yml`) that provides:

- **Manual Trigger**: Workflow dispatch with configurable options
- **Environment Selection**: Choose test environment (production, staging)
- **Test Suite Selection**: Run specific test suites or all tests
- **Artifact Generation**: Automatic report generation and upload
- **Detailed Reporting**: Test summary in GitHub Actions UI

#### Workflow Features:

- ✅ **Flexible Execution**: Choose environment and test suite
- 📊 **Rich Reporting**: HTML and JSON reports with test metrics
- 🔄 **Retry Logic**: Built-in retry for flaky tests
- 📈 **Performance Tracking**: Duration and success rate metrics
- 🎯 **Targeted Testing**: Run specific modules or test categories
- 📤 **Artifact Upload**: Reports stored for 30 days

#### Manual Workflow Trigger:

1. Go to **Actions** tab in GitHub repository
2. Select **RESTful Booker API Test Automation** workflow
3. Click **Run workflow**
4. Configure options:
   - **Environment**: production
   - **Test Suite**: Choose from available options
   - **Generate Artifacts**: Enable/disable report generation

### Local CI Simulation

```bash
# Simulate CI environment locally
export TEST_ENV=production
export API_BASE_URL=https://restful-booker.herokuapp.com
pytest -v --html=reports/ci_report.html --json-report --json-report-file=reports/ci_report.json
```

## 📊 Test Categories

### 1. Authentication Tests (`auth.feature`)

- ✅ Valid credential authentication
- ❌ Invalid credential handling
- 🔒 Token validation and security
- 🚫 Empty credential scenarios

### 2. CRUD Operations (`booking_crud.feature`)

- ➕ **Create**: New booking creation with validation
- 📖 **Read**: Booking retrieval and data verification
- ✏️ **Update**: Full (PUT) and partial (PATCH) updates
- 🗑️ **Delete**: Booking deletion and cleanup
- 🔄 **Workflow**: Complete CRUD lifecycle testing

### 3. Search Operations (`booking_search.feature`)

- 🔍 Search by various criteria
- 📅 Date-based filtering
- 👤 Name-based searches
- 💰 Price range filtering

### 4. Negative Testing (`negative_tests.feature`)

- 🚫 Invalid data handling
- 🔢 Boundary value testing
- 🛡️ Security vulnerability testing
- ⚠️ Error response validation

## 📈 Reporting

### Report Types

The framework generates multiple report formats:

#### 1. HTML Reports

- **Location**: `reports/`
- **Features**: Interactive, self-contained, detailed test results
- **Naming**: `{suite_name}_{timestamp}_report.html`

#### 2. JSON Reports

- **Location**: `reports/`
- **Features**: Machine-readable, integration-friendly
- **Naming**: `{suite_name}_{timestamp}_report.json`

#### 3. Console Output

- **Real-time**: Live test execution feedback
- **Structured**: Organized by test categories
- **Colored**: Success/failure indicators

### Report Analysis

```bash
# View latest HTML report
# Open reports/{latest}_report.html in browser

# Analyze JSON report programmatically
python -c "
import json
with open('reports/{latest}_report.json') as f:
    data = json.load(f)
    print(f'Total: {data[\"summary\"][\"total\"]}')
    print(f'Passed: {data[\"summary\"][\"passed\"]}')
    print(f'Failed: {data[\"summary\"][\"failed\"]}')
"
```

### Custom Reporting

The framework includes advanced reporting capabilities:

```python
# tests/utils/advanced_reporter.py
# Custom metrics and analytics
# Performance trend analysis
# Failure pattern detection
```

## 🛠️ Development

### Adding New Tests

1. **Create Feature File** (BDD approach):

```gherkin
# features/new_feature.feature
Feature: New Feature
    Scenario: Test scenario
        Given precondition
        When action
        Then expected result
```

2. **Implement Step Definitions**:

```python
# tests/step_definitions/test_new_feature.py
from pytest_bdd import scenarios, given, when, then

scenarios('../features/new_feature.feature')

@given('precondition')
def precondition():
    pass

@when('action')
def action():
    pass

@then('expected result')
def expected_result():
    pass
```

3. **Add Test Markers**:

```python
@pytest.mark.smoke
@pytest.mark.positive
def test_function():
    pass
```

### Helper Classes

Extend functionality using helper classes:

```python
# tests/helpers/custom_helper.py
class CustomHelper:
    def __init__(self, api_helper):
        self.api = api_helper

    def custom_operation(self):
        # Implementation
        pass
```

## 🔧 Troubleshooting

### Common Issues

#### 1. **Import Errors**

```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### 2. **API Connection Issues**

```bash
# Check API availability
curl https://restful-booker.herokuapp.com/ping

# Verify environment variables
echo $API_BASE_URL
```

#### 3. **Test Failures**

```bash
# Run with verbose output
pytest -v --tb=long

# Run single test for debugging
pytest tests/step_definitions/test_auth.py::test_specific_function -v -s
```

#### 4. **Report Generation Issues**

```bash
# Ensure reports directory exists
mkdir -p reports

# Check permissions
ls -la reports/
```

### Performance Optimization

```bash
# Use parallel execution
pytest -n auto

# Skip slow tests during development
pytest -m "not performance"

# Use faster assertion introspection
pytest --tb=no
```

### Debugging

```python
# Add debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Use pytest debugging
pytest --pdb  # Drop into debugger on failure
pytest --pdbcls=IPython.terminal.debugger:Pdb  # Use IPython debugger
```

## 📝 Best Practices

### 1. **Test Organization**

- Group related tests in feature files
- Use descriptive scenario names
- Maintain clear test data separation

### 2. **Data Management**

- Use factories for dynamic test data
- Keep static test data in JSON files
- Implement proper test cleanup

### 3. **Error Handling**

- Implement robust retry mechanisms
- Use appropriate timeouts
- Handle network failures gracefully

### 4. **Reporting**

- Generate reports for every test run
- Include performance metrics
- Maintain historical test data
