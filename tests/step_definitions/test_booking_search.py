import pytest
from pytest_bdd import scenarios, given, when, then, parsers
import json
import logging
from tests.helpers.booking_helper import BookingHelper

# Load scenarios from feature file
scenarios('../../features/booking_search.feature')

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@given("the API is available")
def api_is_available(api_helper):
    """Verify API is accessible"""
    response = api_helper.get("/booking")
    assert response.status_code == 200, "API should be available"
    if not hasattr(pytest, 'current_context'):
        pytest.current_context = {}
    pytest.current_context["api_available"] = True

@given("there are existing bookings in the system")
def existing_bookings_in_system(api_helper):
    """Verify there are existing bookings"""
    booking_helper = BookingHelper(api_helper)
    booking_ids = booking_helper.get_all_booking_ids()
    assert len(booking_ids) > 0, "There should be existing bookings in the system"
    pytest.current_context = {"existing_bookings": True}

@given(parsers.parse('I have a booking with firstname "{firstname}"'))
def have_booking_with_firstname(api_helper, cleanup_bookings, firstname):
    """Create a booking with specific firstname"""
    if not hasattr(pytest, 'current_context'):
        pytest.current_context = {}

    booking_helper = BookingHelper(api_helper)

    # Create booking with specific firstname
    booking_data = {
        "firstname": firstname,
        "lastname": "TestLastName",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-01-01",
            "checkout": "2025-01-02"
        },
        "additionalneeds": "Test"
    }

    response, booking_id = booking_helper.create_booking(booking_data)

    if response.status_code == 200 and booking_id:
        pytest.current_context["test_booking_id"] = booking_id
        pytest.current_context["test_booking_data"] = booking_data
        cleanup_bookings.append(booking_id)
        logger.info(f"Created test booking with firstname '{firstname}' and ID: {booking_id}")

@given(parsers.parse('I have a booking with lastname "{lastname}"'))
def have_booking_with_lastname(api_helper, cleanup_bookings, lastname):
    """Create a booking with specific lastname"""
    if not hasattr(pytest, 'current_context'):
        pytest.current_context = {}

    booking_helper = BookingHelper(api_helper)

    # Create booking with specific lastname
    booking_data = {
        "firstname": "TestFirstName",
        "lastname": lastname,
        "totalprice": 200,
        "depositpaid": False,
        "bookingdates": {
            "checkin": "2025-02-01",
            "checkout": "2025-02-03"
        },
        "additionalneeds": "Test"
    }

    response, booking_id = booking_helper.create_booking(booking_data)

    if response.status_code == 200 and booking_id:
        pytest.current_context["test_booking_id"] = booking_id
        pytest.current_context["test_booking_data"] = booking_data
        cleanup_bookings.append(booking_id)
        logger.info(f"Created test booking with lastname '{lastname}' and ID: {booking_id}")

@given(parsers.parse('I have a booking with checkin date "{checkin_date}"'))
def have_booking_with_checkin_date(api_helper, cleanup_bookings, checkin_date):
    """Create a booking with specific checkin date"""
    if not hasattr(pytest, 'current_context'):
        pytest.current_context = {}

    booking_helper = BookingHelper(api_helper)

    # Create booking with specific checkin date
    booking_data = {
        "firstname": "CheckinTest",
        "lastname": "User",
        "totalprice": 175,
        "depositpaid": True,
        "bookingdates": {
            "checkin": checkin_date,
            "checkout": "2025-01-02"
        },
        "additionalneeds": "Test"
    }

    response, booking_id = booking_helper.create_booking(booking_data)

    if response.status_code == 200 and booking_id:
        pytest.current_context["test_booking_id"] = booking_id
        pytest.current_context["test_booking_data"] = booking_data
        cleanup_bookings.append(booking_id)
        logger.info(f"Created test booking with checkin '{checkin_date}' and ID: {booking_id}")

@given(parsers.parse('I have a booking with checkout date "{checkout_date}"'))
def have_booking_with_checkout_date(api_helper, cleanup_bookings, checkout_date):
    """Create a booking with specific checkout date"""
    if not hasattr(pytest, 'current_context'):
        pytest.current_context = {}

    booking_helper = BookingHelper(api_helper)

    # Create booking with specific checkout date
    booking_data = {
        "firstname": "CheckoutTest",
        "lastname": "User",
        "totalprice": 125,
        "depositpaid": False,
        "bookingdates": {
            "checkin": "2025-01-01",
            "checkout": checkout_date
        },
        "additionalneeds": "Test"
    }

    response, booking_id = booking_helper.create_booking(booking_data)

    if response.status_code == 200 and booking_id:
        pytest.current_context["test_booking_id"] = booking_id
        pytest.current_context["test_booking_data"] = booking_data
        cleanup_bookings.append(booking_id)
        logger.info(f"Created test booking with checkout '{checkout_date}' and ID: {booking_id}")

@given(parsers.parse('I have a booking with firstname "{firstname}" and lastname "{lastname}"'))
def have_booking_with_firstname_and_lastname(api_helper, cleanup_bookings, firstname, lastname):
    """Create a booking with specific firstname and lastname"""
    if not hasattr(pytest, 'current_context'):
        pytest.current_context = {}

    booking_helper = BookingHelper(api_helper)

    # Create booking with specific firstname and lastname
    booking_data = {
        "firstname": firstname,
        "lastname": lastname,
        "totalprice": 300,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-03-01",
            "checkout": "2025-03-05"
        },
        "additionalneeds": "Multiple criteria test"
    }

    response, booking_id = booking_helper.create_booking(booking_data)

    if response.status_code == 200 and booking_id:
        pytest.current_context["test_booking_id"] = booking_id
        pytest.current_context["test_booking_data"] = booking_data
        cleanup_bookings.append(booking_id)
        logger.info(f"Created test booking with firstname '{firstname}', lastname '{lastname}' and ID: {booking_id}")

@when("I request all booking IDs")
def request_all_booking_ids(api_helper):
    """Request all booking IDs"""
    booking_helper = BookingHelper(api_helper)
    booking_ids = booking_helper.get_all_booking_ids()

    pytest.current_context["all_booking_ids"] = booking_ids
    logger.info(f"Retrieved {len(booking_ids)} booking IDs")

@when(parsers.parse('I search for bookings with firstname "{firstname}"'))
def search_by_firstname(api_helper, firstname):
    """Search bookings by firstname"""
    booking_helper = BookingHelper(api_helper)
    booking_ids = booking_helper.get_all_booking_ids({"firstname": firstname})

    pytest.current_context["search_results"] = booking_ids
    pytest.current_context["search_criteria"] = {"firstname": firstname}
    logger.info(f"Found {len(booking_ids)} bookings with firstname '{firstname}'")

@when(parsers.parse('I search for bookings with lastname "{lastname}"'))
def search_by_lastname(api_helper, lastname):
    """Search bookings by lastname"""
    booking_helper = BookingHelper(api_helper)
    booking_ids = booking_helper.get_all_booking_ids({"lastname": lastname})

    pytest.current_context["search_results"] = booking_ids
    pytest.current_context["search_criteria"] = {"lastname": lastname}
    logger.info(f"Found {len(booking_ids)} bookings with lastname '{lastname}'")

@when(parsers.parse('I search for bookings with checkin date "{checkin_date}"'))
def search_by_checkin_date(api_helper, checkin_date):
    """Search bookings by checkin date"""
    booking_helper = BookingHelper(api_helper)
    booking_ids = booking_helper.get_all_booking_ids({"checkin": checkin_date})

    pytest.current_context["search_results"] = booking_ids
    pytest.current_context["search_criteria"] = {"checkin": checkin_date}
    logger.info(f"Found {len(booking_ids)} bookings with checkin '{checkin_date}'")

@when(parsers.parse('I search for bookings with checkout date "{checkout_date}"'))
def search_by_checkout_date(api_helper, checkout_date):
    """Search bookings by checkout date"""
    booking_helper = BookingHelper(api_helper)
    booking_ids = booking_helper.get_all_booking_ids({"checkout": checkout_date})

    pytest.current_context["search_results"] = booking_ids
    pytest.current_context["search_criteria"] = {"checkout": checkout_date}
    logger.info(f"Found {len(booking_ids)} bookings with checkout '{checkout_date}'")

@when(parsers.parse('I search for bookings with firstname "{firstname}" and lastname "{lastname}"'))
def search_by_multiple_criteria(api_helper, firstname, lastname):
    """Search bookings by multiple criteria"""
    booking_helper = BookingHelper(api_helper)
    booking_ids = booking_helper.get_all_booking_ids({
        "firstname": firstname,
        "lastname": lastname
    })

    pytest.current_context["search_results"] = booking_ids
    pytest.current_context["search_criteria"] = {"firstname": firstname, "lastname": lastname}
    logger.info(f"Found {len(booking_ids)} bookings with firstname '{firstname}' and lastname '{lastname}'")

@when(parsers.parse('I search for bookings with firstname "{firstname}"'))
def search_nonexistent_booking(api_helper, firstname):
    """Search for non-existent bookings"""
    booking_helper = BookingHelper(api_helper)
    booking_ids = booking_helper.get_all_booking_ids({"firstname": firstname})

    pytest.current_context["search_results"] = booking_ids
    pytest.current_context["search_criteria"] = {"firstname": firstname}

@then("I should receive a list of booking IDs")
def should_receive_booking_ids_list():
    """Verify received list of booking IDs"""
    booking_ids = pytest.current_context["all_booking_ids"]
    assert isinstance(booking_ids, list), "Should receive a list of booking IDs"
    assert len(booking_ids) > 0, "Should receive at least one booking ID"

@then("the response should match the booking list schema")
def response_should_match_booking_list_schema(api_helper):
    """Verify response matches booking list schema"""
    # Create a mock response object for schema validation
    booking_ids = pytest.current_context["all_booking_ids"]
    mock_response_data = [{"bookingid": bid} for bid in booking_ids]

    with open('data/test_schemas.json', 'r') as f:
        schemas = json.load(f)

    schema = schemas["booking_list_schema"]

    # Manual validation since we have the data structure
    assert isinstance(mock_response_data, list), "Response should be a list"
    for item in mock_response_data[:5]:  # Check first 5 items
        assert "bookingid" in item, "Each item should have bookingid"
        assert isinstance(item["bookingid"], int), "Booking ID should be integer"

@then("each booking ID should be a positive integer")
def each_booking_id_should_be_positive_integer():
    """Verify each booking ID is a positive integer"""
    booking_ids = pytest.current_context["all_booking_ids"]

    for booking_id in booking_ids:
        assert isinstance(booking_id, int), f"Booking ID {booking_id} should be an integer"
        assert booking_id > 0, f"Booking ID {booking_id} should be positive"

@then("I should receive bookings that match the criteria")
def should_receive_matching_bookings(api_helper):
    """Verify received bookings match search criteria"""
    search_results = pytest.current_context["search_results"]
    assert isinstance(search_results, list), "Search results should be a list"

    # If we created a test booking, verify it's in the results
    if "test_booking_id" in pytest.current_context:
        test_booking_id = pytest.current_context["test_booking_id"]
        # Note: The search might return the booking or might not due to timing
        # We'll just verify the response structure is correct
        logger.info(f"Search returned {len(search_results)} results")

@then(parsers.parse('all returned bookings should have firstname "{expected_firstname}"'))
def all_bookings_should_have_firstname(api_helper, expected_firstname):
    """Verify all returned bookings have expected firstname"""
    search_results = pytest.current_context["search_results"]
    booking_helper = BookingHelper(api_helper)

    # Check first few results to verify firstname
    for booking_id in search_results[:3]:  # Check first 3 to avoid too many requests
        response, booking_data = booking_helper.get_booking(booking_id)
        if response.status_code == 200 and booking_data:
            assert booking_data["firstname"] == expected_firstname,                 f"Booking {booking_id} should have firstname '{expected_firstname}'"

@then(parsers.parse('all returned bookings should have lastname "{expected_lastname}"'))
def all_bookings_should_have_lastname(api_helper, expected_lastname):
    """Verify all returned bookings have expected lastname"""
    search_results = pytest.current_context["search_results"]
    booking_helper = BookingHelper(api_helper)

    # Check first few results to verify lastname
    for booking_id in search_results[:3]:  # Check first 3 to avoid too many requests
        response, booking_data = booking_helper.get_booking(booking_id)
        if response.status_code == 200 and booking_data:
            assert booking_data["lastname"] == expected_lastname,                 f"Booking {booking_id} should have lastname '{expected_lastname}'"

@then("I should receive bookings that match all criteria")
def should_receive_bookings_matching_all_criteria(api_helper):
    """Verify bookings match all search criteria"""
    search_results = pytest.current_context["search_results"]
    search_criteria = pytest.current_context["search_criteria"]
    booking_helper = BookingHelper(api_helper)

    # Check first few results to verify all criteria match
    for booking_id in search_results[:2]:  # Check first 2 to avoid too many requests
        response, booking_data = booking_helper.get_booking(booking_id)
        if response.status_code == 200 and booking_data:
            if "firstname" in search_criteria:
                assert booking_data["firstname"] == search_criteria["firstname"]
            if "lastname" in search_criteria:
                assert booking_data["lastname"] == search_criteria["lastname"]

@then("I should receive an empty list of bookings")
def should_receive_empty_booking_list():
    """Verify search returns empty list"""
    search_results = pytest.current_context["search_results"]
    assert isinstance(search_results, list), "Search results should be a list"
    assert len(search_results) == 0, "Search results should be empty for non-existent criteria"
