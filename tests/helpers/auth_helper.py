import logging
from typing import Optional
from tests.helpers.api_helper import APIHelper

class AuthHelper:
    """Helper class for authentication operations"""

    def __init__(self, api_helper: APIHelper):
        self.api_helper = api_helper
        self.logger = logging.getLogger(__name__)

    def get_auth_token(self, username: str = "admin", password: str = "password123") -> Optional[str]:
        """
        Get authentication token from the API

        Args:
            username: Username for authentication (default: admin)
            password: Password for authentication (default: password123)

        Returns:
            Authentication token or None if authentication fails
        """
        auth_payload = {
            "username": username,
            "password": password
        }

        try:
            response = self.api_helper.post("/auth", data=auth_payload)

            if response.status_code == 200:
                token = response.json().get("token")
                self.logger.info("Authentication successful")
                return token
            else:
                self.logger.error(f"Authentication failed with status: {response.status_code}")
                return None

        except Exception as e:
            self.logger.error(f"Authentication error: {str(e)}")
            return None

    def validate_token(self, token: str) -> bool:
        """
        Validate if a token is still valid by making an authenticated request

        Args:
            token: Authentication token to validate

        Returns:
            True if token is valid, False otherwise
        """
        headers = {"Cookie": f"token={token}"}

        try:
            # Try to make an authenticated request
            response = self.api_helper.get("/booking/1", headers=headers)
            return response.status_code != 401

        except Exception as e:
            self.logger.error(f"Token validation error: {str(e)}")
            return False

    def get_auth_headers(self, token: str) -> dict:
        """
        Get headers with authentication token

        Args:
            token: Authentication token

        Returns:
            Headers dictionary with authentication
        """
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Cookie": f"token={token}"
        }

    def test_invalid_credentials(self, username: str, password: str) -> bool:
        """
        Test authentication with invalid credentials

        Args:
            username: Invalid username to test
            password: Invalid password to test

        Returns:
            True if authentication properly fails, False otherwise
        """
        token = self.get_auth_token(username, password)
        return token is None
