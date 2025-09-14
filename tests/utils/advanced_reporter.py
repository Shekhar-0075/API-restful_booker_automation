import json
import os
from datetime import datetime
from typing import Dict, List, Optional

class AdvancedTestReporter:
    """Enhanced test reporting with metrics"""
    
    def __init__(self):
        self.test_results = []
        self.performance_data = []
        self.security_results = []
        self.start_time = datetime.now()
    
    def add_test_result(self, test_name: str, status: str, duration: float, details: Optional[Dict] = None):
        """Add test result to reporter"""
        self.test_results.append({
            'test_name': test_name,
            'status': status,
            'duration': duration,
            'timestamp': datetime.now().isoformat(),
            'details': details or {}
        })
    
    def add_performance_data(self, performance_summary: Dict):
        """Add performance data"""
        self.performance_data.append({
            'timestamp': datetime.now().isoformat(),
            'metrics': performance_summary
        })
    
    def add_security_results(self, security_summary: Dict):
        """Add security test results"""
        self.security_results.append({
            'timestamp': datetime.now().isoformat(),
            'results': security_summary
        })
    
    def generate_summary_report(self) -> Dict:
        """Generate comprehensive test summary"""
        end_time = datetime.now()
        total_duration = (end_time - self.start_time).total_seconds()
        
        passed_tests = [t for t in self.test_results if t['status'] == 'PASSED']
        failed_tests = [t for t in self.test_results if t['status'] == 'FAILED']
        
        return {
            'execution_summary': {
                'start_time': self.start_time.isoformat(),
                'end_time': end_time.isoformat(),
                'total_duration': f"{total_duration:.2f}s",
                'total_tests': len(self.test_results),
                'passed': len(passed_tests),
                'failed': len(failed_tests),
                'success_rate': f"{(len(passed_tests) / len(self.test_results) * 100):.1f}%" if self.test_results else "0%"
            },
            'performance_summary': self.performance_data[-1] if self.performance_data else {},
            'security_summary': self.security_results[-1] if self.security_results else {},
            'failed_tests': [{'name': t['test_name'], 'details': t['details']} for t in failed_tests]
        }
    
    def save_enhanced_report(self, file_path: str = "reports/enhanced_summary.json"):
        """Save enhanced report to file"""
        os.makedirs("reports", exist_ok=True)
        
        with open(file_path, 'w') as f:
            json.dump(self.generate_summary_report(), f, indent=2)
        
        print(f"Enhanced report saved: {file_path}")
