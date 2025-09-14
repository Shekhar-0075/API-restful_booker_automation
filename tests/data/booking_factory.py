import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

class BookingDataFactory:
    """Dynamic test data generation for bookings"""
    
    @staticmethod
    def create_valid_booking():
        """Create valid booking data"""
        checkin_date = fake.date_between(start_date="today", end_date="+30d")
        checkout_date = fake.date_between(start_date=checkin_date + timedelta(days=1), end_date="+60d")
        
        return {
            "firstname": fake.first_name(),
            "lastname": fake.last_name(),
            "totalprice": random.randint(50, 2000),
            "depositpaid": fake.boolean(),
            "bookingdates": {
                "checkin": checkin_date.strftime("%Y-%m-%d"),
                "checkout": checkout_date.strftime("%Y-%m-%d")
            },
            "additionalneeds": fake.random_element(elements=("Breakfast", "Lunch", "Dinner", "WiFi", None))
        }
    
    @staticmethod
    def create_invalid_booking(invalid_field="firstname"):
        """Create invalid booking data for negative testing"""
        base_data = BookingDataFactory.create_valid_booking()
        
        invalid_patterns = {
            "firstname": "",
            "lastname": None,
            "totalprice": "not_a_number",
            "depositpaid": "not_boolean",
            "checkin": "invalid_date",
            "checkout": "2020-01-01"  # Past date
        }
        
        if invalid_field in invalid_patterns:
            if invalid_field in ["checkin", "checkout"]:
                base_data["bookingdates"][invalid_field] = invalid_patterns[invalid_field]
            else:
                base_data[invalid_field] = invalid_patterns[invalid_field]
        
        return base_data
    
    @staticmethod
    def create_security_test_booking(attack_type="sql_injection"):
        """Create booking data for security testing"""
        base_data = BookingDataFactory.create_valid_booking()
        
        payloads = {
            "sql_injection": "'; DROP TABLE bookings; --",
            "xss": "<script>alert('XSS')</script>",
            "command_injection": "; ls -la"
        }
        
        # Apply payload to firstname (most common injection point)
        base_data["firstname"] = payloads.get(attack_type, payloads["sql_injection"])
        
        return base_data
