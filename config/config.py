import os
from dataclasses import dataclass
from typing import Dict, Any
import json

@dataclass
class Config:
    """Configuration class for API testing"""

    def __init__(self):
        self.base_url = os.getenv('API_BASE_URL', 'https://restful-booker.herokuapp.com')
        self.environment = os.getenv('TEST_ENV', 'staging')
        self.timeout = int(os.getenv('REQUEST_TIMEOUT', '30'))
        self.retry_count = int(os.getenv('RETRY_COUNT', '3'))
        self.retry_backoff = float(os.getenv('RETRY_BACKOFF', '1.5'))

        # Load environment-specific configurations
        self.env_config = self._load_environment_config()

    def _load_environment_config(self) -> Dict[str, Any]:
        """Load environment specific configuration"""
        try:
            with open('config/environments.json', 'r') as f:
                environments = json.load(f)
                return environments.get(self.environment, {})
        except FileNotFoundError:
            return {}

    @property
    def auth_endpoint(self) -> str:
        return f"{self.base_url}/auth"

    @property  
    def booking_endpoint(self) -> str:
        return f"{self.base_url}/booking"

    def get_headers(self, content_type: str = "application/json") -> Dict[str, str]:
        """Get standard headers for requests"""
        return {
            "Content-Type": content_type,
            "Accept": "application/json"
        }

    def get_auth_headers(self, token: str) -> Dict[str, str]:
        """Get headers with authentication token"""
        headers = self.get_headers()
        headers["Cookie"] = f"token={token}"
        return headers
