#!/usr/bin/env python3
"""
RESTful Booker API Test Runner
Generates HTML and JSON reports for every test execution
"""

import subprocess
import sys
import os
import shutil
import json
from datetime import datetime
from typing import Dict, Tuple

class APITestRunner:  # ✅ CHANGED FROM TestRunner to APITestRunner
    """Simple test runner with essential reporting"""
    
    def __init__(self):
        self.start_time = datetime.now()
        self.reports_dir = "reports"
        
    def clean_reports_folder(self):
        """Clean the reports folder before execution"""
        if os.path.exists(self.reports_dir):
            print("Cleaning reports folder...")
            shutil.rmtree(self.reports_dir)
        
        os.makedirs(self.reports_dir, exist_ok=True)
        

    def run_command(self, command: str, description: str) -> bool:
        """Run a command and handle the result"""
        #print(f"\nRunning: {description}")
        #print(f"Command: {command}")
        print("-" * 50)
        
        try:
            result = subprocess.run(command, shell=True, check=True, capture_output=False)
            print(f"✓ {description} - SUCCESS")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ {description} - FAILED (Exit code: {e.returncode})")
            return False

    def generate_report_filename(self, suite_name: str) -> Tuple[str, str]:
        """Generate timestamped report filenames"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_suite_name = suite_name.replace(" ", "_").lower()
        
        html_file = f"{self.reports_dir}/{safe_suite_name}_{timestamp}_report.html"
        json_file = f"{self.reports_dir}/{safe_suite_name}_{timestamp}_report.json"
        
        return html_file, json_file

    def add_report_flags(self, base_command: str, suite_name: str) -> Tuple[str, str, str]:
        """Add reporting flags to pytest command"""
        html_file, json_file = self.generate_report_filename(suite_name)
        
        report_flags = f" --html={html_file} --self-contained-html --json-report --json-report-file={json_file}"
        
        if "--html=" not in base_command:
            base_command += report_flags
        
        return base_command, html_file, json_file

    def get_test_suites(self) -> Dict:
        """Get test suite configurations"""
        return {
            "1": ("pytest -m smoke -v", "Smoke Tests"),
            "2": ("pytest -m functional -v", "Functional Tests"),
            "3": ("pytest -m security -v", "Non-Functional Tests"),
            "4": ("pytest -m positive -v", "Positive Tests"),
            "5": ("pytest -m negative -v", "Negative Tests"),
            "6": ("pytest tests/step_definitions/test_auth.py -v", "Auth Module Only"),
            "7": ("pytest tests/step_definitions/test_booking_crud.py -v", "CRUD Module Only"),
            "8": ("pytest tests/step_definitions/test_booking_search.py -v", "Search Module Only"),
            "9": ("pytest -v", "All Tests")
        }

    def display_test_suites(self):
        """Display test suite menu"""
        print("Available test suites:")
        test_suites = self.get_test_suites()
        for key, (command, name) in test_suites.items():
            print(f" {key}. {name}")

    def analyze_results(self, json_file: str) -> Dict:
        """Analyze test results from JSON report"""
        try:
            if os.path.exists(json_file):
                with open(json_file, 'r') as f:
                    report_data = json.load(f)
                
                summary = report_data.get('summary', {})
                return {
                    'total': summary.get('total', 0),
                    'passed': summary.get('passed', 0),
                    'failed': summary.get('failed', 0),
                    'duration': summary.get('duration', 0)
                }
        except Exception:
            pass
        
        return {}

    def display_results(self, success: bool, results: Dict, html_file: str, json_file: str):
        """Display execution results"""
        print("\n" + "=" * 50)
        
        if success:
            print("TEST EXECUTION COMPLETED SUCCESSFULLY!")
            
            if results:
                print(f"Total Tests: {results.get('total', 'N/A')}")
                print(f"Passed: {results.get('passed', 'N/A')}")
                print(f"Failed: {results.get('failed', 'N/A')}")
                print(f"Duration: {results.get('duration', 'N/A'):.1f}s")
                
                if results.get('total', 0) > 0:
                    success_rate = (results.get('passed', 0) / results.get('total', 1)) * 100
                    print(f"Success Rate: {success_rate:.1f}%")
            
            print(f"\nReports generated:")
            
            
        else:
            print("TEST EXECUTION FAILED!")
            print(f"Check reports for details:")
            print(f"HTML Report: {html_file}")
            print(f"JSON Report: {json_file}")

    def verify_report_files(self, html_file: str, json_file: str):
        """Verify report files exist"""
        if os.path.exists(html_file):
            print(f"✓ HTML report created ({os.path.getsize(html_file)} bytes)")
        if os.path.exists(json_file):
            print(f"✓ JSON report created ({os.path.getsize(json_file)} bytes)")

    def run_test_suite(self, choice: str) -> bool:
        """Execute the selected test suite"""
        test_suites = self.get_test_suites()
        
        if choice not in test_suites:
            print("Invalid selection!")
            return False
        
        base_command, suite_name = test_suites[choice]
        enhanced_command, html_file, json_file = self.add_report_flags(base_command, suite_name)
        
        print(f"\nExecuting: {suite_name}")
        print(f"HTML Report: {html_file}")
        print(f"JSON Report: {json_file}")
        
        # Run the test suite
        success = self.run_command(enhanced_command, suite_name)
        
        # Analyze and display results
        results = self.analyze_results(json_file)
        self.display_results(success, results, html_file, json_file)
        self.verify_report_files(html_file, json_file)
        
        return success

def main():
    """Main test runner function"""
    print("RESTful Booker API Test Runner")
    print("=" * 40)
    
    # Initialize test runner
    runner = APITestRunner()  # ✅ CHANGED FROM TestRunner to APITestRunner
    
    # Ensure we're in the project directory
    if not os.path.exists("features") or not os.path.exists("tests"):
        print("ERROR: Please run this script from the project root directory")
        sys.exit(1)
    
    # Clean and prepare reports directory
    runner.clean_reports_folder()
    
    # Display test suite menu
    runner.display_test_suites()
    
    # Get user selection
    choice = input("\nSelect test suite (1-9) or 'q' to quit: ").strip()
    
    if choice.lower() == 'q':
        sys.exit(0)
    
    if choice not in [str(i) for i in range(1, 10)]:
        print("Invalid selection!")
        sys.exit(1)
    
    # Execute selected test suite
    success = runner.run_test_suite(choice)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
