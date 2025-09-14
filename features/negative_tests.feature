Feature: Negative Testing and Error Handling
    As a user of the RESTful Booker API
    I want to test error conditions and invalid inputs
    So that I can ensure the API handles edge cases properly

    @negative @security
    Scenario: Create booking with empty first name
        Given I have booking data with empty firstname
        When I attempt to create the booking
        Then the request should fail with appropriate error
        And I should receive a meaningful error message

    @negative @security
    Scenario: Create booking with null last name
        Given I have booking data with null lastname
        When I attempt to create the booking
        Then the request should handle null values appropriately

    @negative @security
    Scenario: Create booking with invalid price type
        Given I have booking data with invalid price type
        When I attempt to create the booking
        Then the request should fail with type validation error

    @negative @security
    Scenario: Create booking with invalid boolean value
        Given I have booking data with invalid depositpaid value
        When I attempt to create the booking
        Then the request should fail with boolean validation error

    @negative @security
    Scenario: Create booking with invalid date format
        Given I have booking data with invalid date format
        When I attempt to create the booking
        Then the request should fail with date validation error

    @negative @security
    Scenario: Create booking with checkout date before checkin date
        Given I have booking data with checkout before checkin
        When I attempt to create the booking
        Then the request should fail with logical date validation error

    @negative @security
    Scenario: Create booking with missing required fields
        Given I have booking data missing required firstname field
        When I attempt to create the booking
        Then the request should fail with missing field error

    @negative @security
    Scenario: Retrieve non-existent booking
        Given I have a non-existent booking ID 99999
        When I attempt to retrieve the booking
        Then I should receive a 404 not found error
        And the response should indicate the booking was not found

    @negative @security @auth
    Scenario: Update booking without authentication
        Given I have an existing booking
        And I do not have authentication token
        When I attempt to update the booking
        Then I should receive a 403 forbidden error
        And the booking should remain unchanged

    @negative @security @auth
    Scenario: Delete booking with invalid token
        Given I have an existing booking
        And I have an invalid authentication token
        When I attempt to delete the booking
        Then I should receive an authentication error
        And the booking should not be deleted

    @negative @security
    Scenario: SQL Injection attempt in booking fields
        Given I have booking data with SQL injection patterns
        When I attempt to create the booking
        Then the API should prevent SQL injection
        And no database corruption should occur

    @negative @security
    Scenario: XSS attempt in booking fields
        Given I have booking data with XSS script patterns
        When I attempt to create the booking
        Then the API should sanitize the input
        And no script execution should occur
