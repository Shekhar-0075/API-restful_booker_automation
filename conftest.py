import pytest
import requests
import json
import logging
from faker import Faker
from typing import Dict, Any, List
from tests.helpers.api_helper import APIHelper
from tests.helpers.auth_helper import AuthHelper
from tests.helpers.booking_helper import BookingHelper
from config.config import Config

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

fake = Faker()

@pytest.fixture(scope="session")
def config():
    """Load configuration for tests"""
    return Config()

@pytest.fixture(scope="session")
def api_helper(config):
    """Create API helper instance"""
    return APIHelper(config.base_url, timeout=config.timeout, retry_count=config.retry_count)

@pytest.fixture(scope="session")
def auth_helper(api_helper):
    """Create authentication helper instance"""
    return AuthHelper(api_helper)

@pytest.fixture(scope="session")
def booking_helper(api_helper):
    """Create booking helper instance"""
    return BookingHelper(api_helper)

@pytest.fixture(scope="session")
def auth_token(auth_helper):
    """Get authentication token for the session"""
    token = auth_helper.get_auth_token("admin", "password123")
    if not token:
        pytest.fail("Failed to obtain authentication token")
    return token

@pytest.fixture
def booking_payload():
    """Generate random booking payload"""
    checkin_date = fake.date_between(start_date="today", end_date="+30d")
    checkout_date = fake.date_between(start_date=checkin_date, end_date="+60d")
    
    return {
        "firstname": fake.first_name(),
        "lastname": fake.last_name(),
        "totalprice": fake.random_int(min=50, max=2000),
        "depositpaid": fake.boolean(),
        "bookingdates": {
            "checkin": checkin_date.strftime("%Y-%m-%d"),
            "checkout": checkout_date.strftime("%Y-%m-%d")
        },
        "additionalneeds": fake.random_element(elements=("Breakfast", "Lunch", "Dinner", "WiFi", None))
    }

@pytest.fixture
def invalid_booking_payload():
    """Generate invalid booking payload for negative tests"""
    return {
        "firstname": "",
        "lastname": None,
        "totalprice": "invalid_price",
        "depositpaid": "not_boolean",
        "bookingdates": {
            "checkin": "invalid_date",
            "checkout": "2022-01-01"  # Past date
        }
    }

@pytest.fixture
def test_data():
    """Load test data from JSON files"""
    test_data = {}
    try:
        with open('data/booking_data.json', 'r') as f:
            test_data['booking_data'] = json.load(f)
    except FileNotFoundError:
        test_data['booking_data'] = {}

    try:
        with open('data/invalid_data.json', 'r') as f:
            test_data['invalid_data'] = json.load(f)
    except FileNotFoundError:
        test_data['invalid_data'] = {}

    try:
        with open('data/test_schemas.json', 'r') as f:
            test_data['schemas'] = json.load(f)
    except FileNotFoundError:
        test_data['schemas'] = {}

    return test_data

@pytest.fixture
def cleanup_bookings():
    """Cleanup created bookings after tests"""
    created_booking_ids = []
    yield created_booking_ids
    
    if created_booking_ids:
        logging.info(f"Created booking IDs during test: {created_booking_ids}")

@pytest.fixture(autouse=True)
def setup_test_context():
    """Setup test context for each test"""
    pytest.current_context = {}
    yield
    
    if hasattr(pytest, 'current_context'):
        delattr(pytest, 'current_context')

@pytest.fixture
def performance_threshold():
    """Define performance thresholds for API calls"""
    return {
        "create_booking": 5000,
        "get_booking": 3000,
        "update_booking": 5000,
        "delete_booking": 3000,
        "get_all_bookings": 10000
    }

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results for reporting"""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call":
        if hasattr(pytest, 'current_context'):
            report.user_properties = getattr(report, 'user_properties', [])
            context_data = getattr(pytest, 'current_context', {})
            for key, value in context_data.items():
                if isinstance(value, (str, int, float, bool)):
                    report.user_properties.append((key, value))

def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line("markers", "smoke: Smoke tests - Critical functionality")
    config.addinivalue_line("markers", "regression: Regression tests - Full test suite")
    config.addinivalue_line("markers", "functional: Functional tests - Feature testing")
    config.addinivalue_line("markers", "security: Security tests - Security validation")
    config.addinivalue_line("markers", "performance: Performance tests - Response time validation")
    config.addinivalue_line("markers", "negative: Negative tests - Error condition testing")
    config.addinivalue_line("markers", "positive: Positive tests - Happy path scenarios")
    config.addinivalue_line("markers", "auth: Authentication tests - Token and auth testing")
    config.addinivalue_line("markers", "booking: Booking related tests - Booking operations")
    config.addinivalue_line("markers", "crud: CRUD operation tests - Create, Read, Update, Delete")
    config.addinivalue_line("markers", "search: Search operation tests - Query and filtering")

def pytest_collection_modifyitems(config, items):
    """Modify test collection to add default markers"""
    for item in items:
        if "test_auth" in item.nodeid:
            item.add_marker(pytest.mark.auth)
        if "test_booking" in item.nodeid:
            item.add_marker(pytest.mark.booking)
        if "negative" in item.nodeid:
            item.add_marker(pytest.mark.negative)
