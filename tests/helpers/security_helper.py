import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class SecurityTestHelper:
    """Security testing utilities"""
    
    COMMON_PAYLOADS = {
        'sql_injection': [
            "'; DROP TABLE bookings; --",
            "1' OR '1'='1",
            "admin'--",
            "1; SELECT * FROM users"
        ],
        'xss_payloads': [
            "<script>alert('XSS')</script>",
            "javascript:alert('XSS')",
            "<img src=x onerror=alert('XSS')>",
            "'-alert('XSS')-'"
        ],
        'command_injection': [
            "; ls -la",
            "| whoami", 
            "&& cat /etc/passwd"
        ]
    }
    
    def test_input_validation(self, api_helper, endpoint: str, field: str, payload_type: str = 'sql_injection') -> List[Dict]:
        """Test input validation against common attacks"""
        results = []
        payloads = self.COMMON_PAYLOADS.get(payload_type, self.COMMON_PAYLOADS['sql_injection'])
        
        for payload in payloads:
            test_data = {field: payload, "lastname": "TestUser", "totalprice": 100, "depositpaid": True,
                        "bookingdates": {"checkin": "2025-01-01", "checkout": "2025-01-02"}}
            
            try:
                response = api_helper.post(endpoint, data=test_data)
                is_vulnerable = self._analyze_security_response(response, payload_type)
                
                results.append({
                    'payload': payload,
                    'status_code': response.status_code,
                    'response_length': len(response.text),
                    'potentially_vulnerable': is_vulnerable,
                    'response_time': getattr(response, 'elapsed', None)
                })
                
                logger.info(f"Security test - Payload: {payload[:20]}... Status: {response.status_code}")
                
            except Exception as e:
                results.append({
                    'payload': payload,
                    'error': str(e),
                    'potentially_vulnerable': False
                })
        
        return results
    
    def _analyze_security_response(self, response, payload_type: str) -> bool:
        """Analyze response for potential vulnerabilities"""
        response_text = response.text.lower()
        
        # Common vulnerability indicators
        vulnerability_indicators = {
            'sql_injection': ['syntax error', 'mysql', 'postgresql', 'sqlite', 'ora-'],
            'xss_payloads': ['<script', 'javascript:', 'onerror'],
            'command_injection': ['command not found', '/bin/', 'permission denied']
        }
        
        indicators = vulnerability_indicators.get(payload_type, [])
        return any(indicator in response_text for indicator in indicators)
    
    def generate_security_report(self, test_results: List[Dict]) -> Dict:
        """Generate security test report"""
        total_tests = len(test_results)
        vulnerable_count = sum(1 for result in test_results if result.get('potentially_vulnerable', False))
        
        return {
            'total_security_tests': total_tests,
            'potentially_vulnerable_responses': vulnerable_count,
            'security_score': f"{((total_tests - vulnerable_count) / total_tests * 100):.1f}%",
            'recommendations': self._get_security_recommendations(vulnerable_count)
        }
    
    def _get_security_recommendations(self, vulnerable_count: int) -> List[str]:
        """Get security recommendations based on test results"""
        if vulnerable_count == 0:
            return ["No obvious security vulnerabilities detected", "Continue regular security testing"]
        else:
            return [
                "Potential security vulnerabilities detected",
                "Review input validation and sanitization",
                "Consider implementing rate limiting",
                "Add comprehensive logging for security events"
            ]
