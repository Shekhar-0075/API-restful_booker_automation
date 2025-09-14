Feature: Booking CRUD Operations
    As a user of the RESTful Booker API
    I want to create, read, update, and delete bookings
    So that I can manage hotel reservations

    Background:
        Given the API is available
        And I have valid authentication token

    @smoke @positive @crud @booking
    Scenario: Create a new booking with valid data
        Given I have valid booking data
        When I create a new booking
        Then the booking should be created successfully
        And I should receive a booking ID
        And the response should match the booking creation schema

    @functional @positive @crud @booking
    Scenario: Retrieve an existing booking by ID
        Given I have created a booking
        When I retrieve the booking by its ID
        Then I should get the booking details
        And the booking data should match what was created
        And the response should match the booking detail schema

    @functional @positive @crud @booking
    Scenario: Update an entire booking using PUT
        Given I have created a booking
        And I have updated booking data
        When I update the entire booking using PUT
        Then the booking should be updated successfully
        And all fields should reflect the new values

    @functional @positive @crud @booking
    Scenario: Partially update a booking using PATCH
        Given I have created a booking
        And I have partial update data
        When I partially update the booking using PATCH
        Then only the specified fields should be updated
        And other fields should remain unchanged

    @functional @positive @crud @booking
    Scenario: Delete an existing booking
        Given I have created a booking
        When I delete the booking
        Then the booking should be deleted successfully
        And the booking should no longer be retrievable

    @functional @positive @crud @booking
    Scenario: Complete CRUD workflow
        Given I have valid booking data
        When I create a new booking
        And I retrieve the booking by its ID
        And I update the booking
        And I delete the booking
        Then all operations should complete successfully
