Feature: Booking Search and Filtering
    As a user of the RESTful Booker API
    I want to search and filter bookings
    So that I can find specific reservations

    @functional @positive @booking @search
    Scenario: Get all booking IDs
        Given the API is available
        When I request all booking IDs
        Then I should receive a list of booking IDs
        And the response should match the booking list schema
        And each booking ID should be a positive integer

    @functional @positive @booking @search
    Scenario: Search bookings by first name
        Given there are existing bookings in the system
        And I have a booking with firstname "John"
        When I search for bookings with firstname "John"
        Then I should receive bookings that match the criteria
        And all returned bookings should have firstname "John"

    @functional @positive @booking @search
    Scenario: Search bookings by last name
        Given there are existing bookings in the system
        And I have a booking with lastname "Doe"
        When I search for bookings with lastname "Doe"
        Then I should receive bookings that match the criteria
        And all returned bookings should have lastname "Doe"

    @functional @positive @booking @search
    Scenario: Search bookings by check-in date
        Given there are existing bookings in the system
        And I have a booking with checkin date "2025-01-01"
        When I search for bookings with checkin date "2025-01-01"
        Then I should receive bookings that match the criteria

    @functional @positive @booking @search
    Scenario: Search bookings by check-out date
        Given there are existing bookings in the system
        And I have a booking with checkout date "2025-01-02"
        When I search for bookings with checkout date "2025-01-02"
        Then I should receive bookings that match the criteria

    @functional @positive @booking @search
    Scenario: Search bookings with multiple criteria
        Given there are existing bookings in the system
        And I have a booking with firstname "John" and lastname "Doe"
        When I search for bookings with firstname "John" and lastname "Doe"
        Then I should receive bookings that match all criteria

    @functional @negative @booking @search
    Scenario: Search with non-existent criteria returns empty results
        Given the API is available
        When I search for bookings with firstname "NonExistent"
        Then I should receive an empty list of bookings
