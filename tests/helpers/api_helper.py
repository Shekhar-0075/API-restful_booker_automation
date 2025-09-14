import requests
import time
import logging
from typing import Dict, Any, Optional, Union
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

import json

class APIHelper:
    """Helper class for API operations with robust error handling"""

    def __init__(self, base_url: str, timeout: int = 30, retry_count: int = 3):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = self._create_session(retry_count)
        self.logger = logging.getLogger(__name__)

    def _create_session(self, retry_count: int) -> requests.Session:
        """Create requests session with retry strategy"""
        session = requests.Session()

        retry_strategy = Retry(
            total=retry_count,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "PATCH", "DELETE"]
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        return session

    def make_request(
        self, 
        method: str, 
        endpoint: str, 
        headers: Optional[Dict[str, str]] = None,
        data: Optional[Union[Dict, str]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> requests.Response:
        """Make HTTP request with error handling"""

        url = f"{self.base_url}{endpoint}"

        # Default headers
        default_headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if headers:
            default_headers.update(headers)

        try:
            self.logger.info(f"Making {method} request to {url}")
            if data:
                self.logger.debug(f"Request data: {data}")

            response = self.session.request(
                method=method.upper(),
                url=url,
                headers=default_headers,
                json=data if isinstance(data, dict) else None,
                data=data if isinstance(data, str) else None,
                params=params,
                timeout=self.timeout
            )

            self.logger.info(f"Response status: {response.status_code}")
            if response.status_code >= 400:
                self.logger.error(f"Error response: {response.text}")

            return response

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed: {str(e)}")
            raise

    def get(self, endpoint: str, headers: Optional[Dict] = None, params: Optional[Dict] = None) -> requests.Response:
        """Make GET request"""
        return self.make_request("GET", endpoint, headers, params=params)

    def post(self, endpoint: str, data: Optional[Dict] = None, headers: Optional[Dict] = None) -> requests.Response:
        """Make POST request"""
        return self.make_request("POST", endpoint, headers, data)

    def put(self, endpoint: str, data: Optional[Dict] = None, headers: Optional[Dict] = None) -> requests.Response:
        """Make PUT request"""
        return self.make_request("PUT", endpoint, headers, data)

    def patch(self, endpoint: str, data: Optional[Dict] = None, headers: Optional[Dict] = None) -> requests.Response:
        """Make PATCH request"""
        return self.make_request("PATCH", endpoint, headers, data)

    def delete(self, endpoint: str, headers: Optional[Dict] = None) -> requests.Response:
        """Make DELETE request"""
        return self.make_request("DELETE", endpoint, headers)

    def validate_response_schema(self, response: requests.Response, expected_schema: Dict) -> bool:
        """Validate response against JSON schema"""
        try:
            import jsonschema
            response_data = response.json()
            jsonschema.validate(response_data, expected_schema)
            self.logger.info("Schema validation passed")
            return True
        except jsonschema.ValidationError as e:
            self.logger.error(f"Schema validation failed: {str(e)}")
            return False
        except ValueError as e:
            self.logger.error(f"Invalid JSON response: {str(e)}")
            return False

    def measure_response_time(self, method: str, endpoint: str, **kwargs) -> tuple:
        """Measure response time for performance testing"""
        start_time = time.time()
        response = self.make_request(method, endpoint, **kwargs)
        end_time = time.time()

        response_time = (end_time - start_time) * 1000  # Convert to milliseconds
        self.logger.info(f"Response time: {response_time:.2f}ms")
        return response, response_time

    def check_api_health(self) -> bool:
        """Check if API is healthy and accessible"""
        try:
            response = self.get("/booking")
            return response.status_code == 200
        except Exception as e:
            self.logger.error(f"API health check failed: {str(e)}")
            return False
