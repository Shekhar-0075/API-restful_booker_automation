import logging
from typing import Dict, List, Optional, Any
from tests.helpers.api_helper import APIHelper

class BookingHelper:
    """Helper class for booking-related operations"""

    def __init__(self, api_helper: APIHelper):
        self.api_helper = api_helper
        self.logger = logging.getLogger(__name__)

    def create_booking(self, booking_data: Dict[str, Any]) -> tuple:
        """Create a new booking"""
        try:
            response = self.api_helper.post("/booking", data=booking_data)
            if response.status_code == 200:
                booking_id = response.json().get("bookingid")
                self.logger.info(f"Booking created successfully with ID: {booking_id}")
                return response, booking_id
            else:
                self.logger.error(f"Booking creation failed with status: {response.status_code}")
                return response, None
        except Exception as e:
            self.logger.error(f"Error creating booking: {str(e)}")
            raise

    def get_booking(self, booking_id: int) -> tuple:
        """Get booking by ID"""
        try:
            response = self.api_helper.get(f"/booking/{booking_id}")
            if response.status_code == 200:
                booking_data = response.json()
                self.logger.info(f"Retrieved booking {booking_id}")
                return response, booking_data
            else:
                self.logger.error(f"Failed to get booking {booking_id}, status: {response.status_code}")
                return response, None
        except Exception as e:
            self.logger.error(f"Error retrieving booking {booking_id}: {str(e)}")
            raise

    def update_booking(self, booking_id: int, booking_data: Dict[str, Any], auth_headers: Dict[str, str], partial: bool = False) -> tuple:
        """Update booking (PUT or PATCH)"""
        try:
            method = "PATCH" if partial else "PUT"
            endpoint = f"/booking/{booking_id}"

            if method == "PUT":
                response = self.api_helper.put(endpoint, data=booking_data, headers=auth_headers)
            else:
                response = self.api_helper.patch(endpoint, data=booking_data, headers=auth_headers)

            if response.status_code == 200:
                updated_data = response.json()
                self.logger.info(f"Booking {booking_id} updated successfully using {method}")
                return response, updated_data
            else:
                self.logger.error(f"Failed to update booking {booking_id}, status: {response.status_code}")
                return response, None
        except Exception as e:
            self.logger.error(f"Error updating booking {booking_id}: {str(e)}")
            raise

    def delete_booking(self, booking_id: int, auth_headers: Dict[str, str]) -> bool:
        """Delete booking"""
        try:
            response = self.api_helper.delete(f"/booking/{booking_id}", headers=auth_headers)
            if response.status_code in [200, 201]:
                self.logger.info(f"Booking {booking_id} deleted successfully")
                return True
            else:
                self.logger.error(f"Failed to delete booking {booking_id}, status: {response.status_code}")
                return False
        except Exception as e:
            self.logger.error(f"Error deleting booking {booking_id}: {str(e)}")
            return False

    def get_all_booking_ids(self, filters: Optional[Dict[str, str]] = None) -> List[int]:
        """Get all booking IDs with optional filters"""
        try:
            response = self.api_helper.get("/booking", params=filters)
            if response.status_code == 200:
                bookings = response.json()
                booking_ids = [booking["bookingid"] for booking in bookings]
                self.logger.info(f"Retrieved {len(booking_ids)} booking IDs")
                return booking_ids
            else:
                self.logger.error(f"Failed to get booking IDs, status: {response.status_code}")
                return []
        except Exception as e:
            self.logger.error(f"Error retrieving booking IDs: {str(e)}")
            return []

    def search_bookings(self, **filters) -> List[Dict]:
        """Search bookings with filters and return full booking data"""
        booking_ids = self.get_all_booking_ids(filters)
        bookings = []

        for booking_id in booking_ids[:5]:  # Limit to first 5 to avoid too many requests
            response, booking_data = self.get_booking(booking_id)
            if booking_data:
                booking_data['bookingid'] = booking_id
                bookings.append(booking_data)

        return bookings
