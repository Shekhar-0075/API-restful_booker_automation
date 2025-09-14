import pytest
from pytest_bdd import scenarios, given, when, then, parsers
import json
import logging
from tests.helpers.booking_helper import BookingHelper

# Load scenarios from feature file
scenarios('../../features/booking_crud.feature')

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@given("the API is available")
def api_is_available(api_helper):
    """Verify API is accessible"""
    response = api_helper.get("/booking")
    assert response.status_code == 200, "API should be available"
    pytest.current_context = {"api_available": True}

@given("I have valid authentication token")
def have_valid_auth_token(auth_token):
    """Store valid authentication token"""
    if not hasattr(pytest, 'current_context'):
        pytest.current_context = {}
    pytest.current_context["auth_token"] = auth_token
    pytest.current_context["auth_headers"] = {
        "Content-Type": "application/json",
        "Accept": "application/json", 
        "Cookie": f"token={auth_token}"
    }

@given("I have valid booking data")
def have_valid_booking_data(booking_payload):
    """Store valid booking data in context"""
    if not hasattr(pytest, 'current_context'):
        pytest.current_context = {}
    pytest.current_context["booking_data"] = booking_payload
    logger.info(f"Using booking data: {booking_payload}")

@given("I have created a booking")
def have_created_booking(api_helper, booking_payload, cleanup_bookings):
    """Create a booking for testing"""
    if not hasattr(pytest, 'current_context'):
        pytest.current_context = {}

    booking_helper = BookingHelper(api_helper)
    response, booking_id = booking_helper.create_booking(booking_payload)

    assert response.status_code == 200, f"Booking creation failed with status {response.status_code}"
    assert booking_id is not None, "Booking ID should not be None"

    # Store created booking info
    pytest.current_context["created_booking_id"] = booking_id
    pytest.current_context["created_booking_data"] = booking_payload
    cleanup_bookings.append(booking_id)

    logger.info(f"Created booking with ID: {booking_id}")

@given("I have updated booking data")
def have_updated_booking_data():
    """Store updated booking data"""
    updated_data = {
        "firstname": "UpdatedFirstName",
        "lastname": "UpdatedLastName", 
        "totalprice": 250,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-03-01",
            "checkout": "2025-03-05"
        },
        "additionalneeds": "Updated needs"
    }
    pytest.current_context["updated_booking_data"] = updated_data

@given("I have partial update data")
def have_partial_update_data():
    """Store partial update data"""
    partial_data = {
        "firstname": "PartiallyUpdated",
        "totalprice": 300
    }
    pytest.current_context["partial_update_data"] = partial_data

@when("I create a new booking")
def create_new_booking(api_helper, cleanup_bookings):
    """Create a new booking"""
    booking_helper = BookingHelper(api_helper)
    booking_data = pytest.current_context["booking_data"]

    response, booking_id = booking_helper.create_booking(booking_data)

    pytest.current_context["create_response"] = response
    pytest.current_context["created_booking_id"] = booking_id

    if booking_id:
        cleanup_bookings.append(booking_id)

@when("I retrieve the booking by its ID")
def retrieve_booking_by_id(api_helper):
    """Retrieve booking by ID"""
    booking_helper = BookingHelper(api_helper)
    booking_id = pytest.current_context["created_booking_id"]

    response, booking_data = booking_helper.get_booking(booking_id)

    pytest.current_context["retrieve_response"] = response
    pytest.current_context["retrieved_booking_data"] = booking_data

@when("I update the entire booking using PUT")
def update_booking_with_put(api_helper):
    """Update booking using PUT method"""
    booking_helper = BookingHelper(api_helper)
    booking_id = pytest.current_context["created_booking_id"]
    updated_data = pytest.current_context["updated_booking_data"]
    auth_headers = pytest.current_context["auth_headers"]

    response, updated_booking = booking_helper.update_booking(
        booking_id, updated_data, auth_headers, partial=False
    )

    pytest.current_context["update_response"] = response
    pytest.current_context["updated_booking_result"] = updated_booking

@when("I partially update the booking using PATCH")
def partially_update_booking_with_patch(api_helper):
    """Update booking using PATCH method"""
    booking_helper = BookingHelper(api_helper)
    booking_id = pytest.current_context["created_booking_id"]
    partial_data = pytest.current_context["partial_update_data"]
    auth_headers = pytest.current_context["auth_headers"]

    response, updated_booking = booking_helper.update_booking(
        booking_id, partial_data, auth_headers, partial=True
    )

    pytest.current_context["patch_response"] = response
    pytest.current_context["patched_booking_result"] = updated_booking

@when("I delete the booking")
def delete_booking(api_helper):
    """Delete the booking"""
    booking_helper = BookingHelper(api_helper)
    booking_id = pytest.current_context["created_booking_id"]
    auth_headers = pytest.current_context["auth_headers"]

    success = booking_helper.delete_booking(booking_id, auth_headers)
    pytest.current_context["delete_success"] = success



@when("I update the booking")
def update_booking_general(api_helper):
    """General booking update for workflow scenarios"""
    booking_helper = BookingHelper(api_helper)
    booking_id = pytest.current_context["created_booking_id"]
    auth_headers = pytest.current_context["auth_headers"]
    
    # FIX: Use booking_data instead of created_booking_data
    original_booking = pytest.current_context.get("booking_data", {})
    
    # Use simple update data for workflow
    update_data = {
        "firstname": "WorkflowUpdated",
        "lastname": original_booking.get("lastname", "DefaultLastName"),
        "totalprice": 199,
        "depositpaid": True,
        "bookingdates": original_booking.get("bookingdates", {
            "checkin": "2025-01-01",
            "checkout": "2025-01-02"
        })
    }
    
    response, updated_booking = booking_helper.update_booking(
        booking_id, update_data, auth_headers, partial=False
    )
    
    pytest.current_context["workflow_update_response"] = response


@then("the booking should be created successfully")
def booking_should_be_created_successfully():
    """Verify booking was created successfully"""
    response = pytest.current_context["create_response"]
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

@then("I should receive a booking ID")
def should_receive_booking_id():
    """Verify booking ID was received"""
    booking_id = pytest.current_context["created_booking_id"]
    assert booking_id is not None, "Booking ID should not be None"
    assert isinstance(booking_id, int), "Booking ID should be an integer"
    assert booking_id > 0, "Booking ID should be positive"

@then("the response should match the booking creation schema")
def response_should_match_creation_schema(api_helper):
    """Verify response matches creation schema"""
    response = pytest.current_context["create_response"]

    # Load schema
    with open('data/test_schemas.json', 'r') as f:
        schemas = json.load(f)

    schema = schemas["booking_response_schema"]
    is_valid = api_helper.validate_response_schema(response, schema)
    assert is_valid, "Response should match booking creation schema"

@then("I should get the booking details")
def should_get_booking_details():
    """Verify booking details were retrieved"""
    response = pytest.current_context["retrieve_response"]
    booking_data = pytest.current_context["retrieved_booking_data"]

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert booking_data is not None, "Booking data should not be None"

@then("the booking data should match what was created")
def booking_data_should_match_created():
    """Verify retrieved data matches created data"""
    created_data = pytest.current_context["created_booking_data"]
    retrieved_data = pytest.current_context["retrieved_booking_data"]

    assert retrieved_data["firstname"] == created_data["firstname"]
    assert retrieved_data["lastname"] == created_data["lastname"]
    assert retrieved_data["totalprice"] == created_data["totalprice"]
    assert retrieved_data["depositpaid"] == created_data["depositpaid"]

@then("the response should match the booking detail schema")
def response_should_match_detail_schema(api_helper):
    """Verify response matches detail schema"""
    response = pytest.current_context["retrieve_response"]

    with open('data/test_schemas.json', 'r') as f:
        schemas = json.load(f)

    schema = schemas["booking_detail_schema"]
    is_valid = api_helper.validate_response_schema(response, schema)
    assert is_valid, "Response should match booking detail schema"

@then("the booking should be updated successfully")
def booking_should_be_updated_successfully():
    """Verify booking was updated successfully"""
    response = pytest.current_context["update_response"]
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

@then("all fields should reflect the new values")
def all_fields_should_reflect_new_values():
    """Verify all fields were updated"""
    updated_data = pytest.current_context["updated_booking_data"]
    result = pytest.current_context["updated_booking_result"]

    assert result["firstname"] == updated_data["firstname"]
    assert result["lastname"] == updated_data["lastname"]
    assert result["totalprice"] == updated_data["totalprice"]

@then("only the specified fields should be updated")
def only_specified_fields_should_be_updated():
    """Verify only specified fields were updated"""
    partial_data = pytest.current_context["partial_update_data"]
    result = pytest.current_context["patched_booking_result"]

    # Check updated fields
    assert result["firstname"] == partial_data["firstname"]
    assert result["totalprice"] == partial_data["totalprice"]

@then("other fields should remain unchanged")
def other_fields_should_remain_unchanged():
    """Verify other fields remained unchanged"""
    original_data = pytest.current_context["created_booking_data"]
    result = pytest.current_context["patched_booking_result"]

    # Check unchanged fields
    assert result["lastname"] == original_data["lastname"]
    assert result["depositpaid"] == original_data["depositpaid"]

@then("the booking should be deleted successfully")
def booking_should_be_deleted_successfully():
    """Verify booking was deleted successfully"""
    success = pytest.current_context["delete_success"]
    assert success, "Booking deletion should be successful"

@then("the booking should no longer be retrievable")
def booking_should_not_be_retrievable(api_helper):
    """Verify booking is no longer retrievable"""
    booking_helper = BookingHelper(api_helper)
    booking_id = pytest.current_context["created_booking_id"]

    response, booking_data = booking_helper.get_booking(booking_id)
    assert response.status_code == 404, "Deleted booking should return 404"

@then("all operations should complete successfully")
def all_operations_should_complete_successfully():
    """Verify all CRUD operations completed successfully"""
    context = pytest.current_context

    # Check creation
    assert context.get("create_response").status_code == 200
    assert context.get("created_booking_id") is not None

    # Check retrieval
    assert context.get("retrieve_response").status_code == 200
    assert context.get("retrieved_booking_data") is not None

    # Check update
    assert context.get("workflow_update_response").status_code == 200

    # Check deletion
    assert context.get("delete_success") is True

    logger.info("All CRUD operations completed successfully")
