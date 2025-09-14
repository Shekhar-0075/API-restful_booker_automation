import pytest
from pytest_bdd import scenarios, given, when, then, parsers
import json
import logging

# Load scenarios from feature file
scenarios('../../features/auth.feature')

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@given("I have valid admin credentials")
def valid_admin_credentials(auth_helper):
    """Store valid admin credentials in context"""
    pytest.current_context = {
        "username": "admin", 
        "password": "password123"
    }

@given(parsers.parse('I have invalid credentials with username "{username}" and password "{password}"'))
def invalid_credentials(username, password):
    """Store invalid credentials in context"""
    pytest.current_context = {
        "username": username,
        "password": password
    }

@given("I have empty credentials")
def empty_credentials():
    """Store empty credentials in context"""
    pytest.current_context = {
        "username": "",
        "password": ""
    }

@given("I have a valid authentication token")
def valid_auth_token(auth_token):
    """Store valid authentication token in context"""
    pytest.current_context = {"token": auth_token}

@when("I request an authentication token")
def request_auth_token(auth_helper):
    """Request authentication token with stored credentials"""
    context = pytest.current_context
    token = auth_helper.get_auth_token(
        context["username"], 
        context["password"]
    )

    # Store token and response in context
    pytest.current_context.update({
        "token": token,
        "auth_successful": token is not None
    })

@when("I use the token to access protected resources")
def use_token_for_protected_access(api_helper):
    """Use token to access a protected resource"""
    context = pytest.current_context
    token = context.get("token")

    if token:
        headers = {"Cookie": f"token={token}"}
        # Try to access a protected endpoint (we'll use GET /booking/1 as test)
        response = api_helper.get("/booking/1", headers=headers)
        pytest.current_context["protected_access_response"] = response
    else:
        pytest.current_context["protected_access_response"] = None

@then("I should receive a valid token")
def should_receive_valid_token():
    """Verify that a valid token was received"""
    context = pytest.current_context
    assert context.get("auth_successful", False), "Authentication should have succeeded"
    assert context.get("token") is not None, "Token should not be None"

@then("the token should be a non-empty string")
def token_should_be_non_empty_string():
    """Verify token is a non-empty string"""
    context = pytest.current_context
    token = context.get("token")
    assert isinstance(token, str), "Token should be a string"
    assert len(token) > 0, "Token should not be empty"

@then("authentication should fail")
def authentication_should_fail():
    """Verify that authentication failed"""
    context = pytest.current_context
    assert not context.get("auth_successful", True), "Authentication should have failed"

@then("I should not receive a token")
def should_not_receive_token():
    """Verify that no token was received"""
    context = pytest.current_context
    assert context.get("token") is None, "Token should be None for failed authentication"

@then("I should receive an error response")
def should_receive_error_response():
    """Verify that an error response was received"""
    context = pytest.current_context
    assert not context.get("auth_successful", True), "Should receive error response"

@then("the token should be accepted")
def token_should_be_accepted():
    """Verify that the token is accepted for protected resources"""
    context = pytest.current_context
    response = context.get("protected_access_response")
    assert response is not None, "Should have received a response"
    assert response.status_code != 401, "Token should be accepted (not 401 Unauthorized)"

@then("I should be able to perform authorized operations")
def should_perform_authorized_operations():
    """Verify that authorized operations can be performed"""
    context = pytest.current_context
    response = context.get("protected_access_response")
    assert response is not None, "Should have received a response"
    # For RESTful Booker, a successful GET request indicates the token works
    assert response.status_code in [200, 404], "Should be able to access protected resources"
