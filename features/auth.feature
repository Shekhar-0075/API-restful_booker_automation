Feature: Authentication
    As a user of the RESTful Booker API
    I want to authenticate and manage tokens
    So that I can perform authorized operations

    @smoke @positive @auth
    Scenario: Generate authentication token with valid credentials
        Given I have valid admin credentials
        When I request an authentication token
        Then I should receive a valid token
        And the token should be a non-empty string

    @negative @auth
    Scenario: Authentication fails with invalid credentials
        Given I have invalid credentials with username "invalid" and password "wrong"
        When I request an authentication token
        Then authentication should fail
        And I should not receive a token

    @negative @auth
    Scenario: Authentication fails with empty credentials
        Given I have empty credentials
        When I request an authentication token
        Then authentication should fail
        And I should receive an error response

    @positive @security @auth
    Scenario: Token validation for authorized operations
        Given I have a valid authentication token
        When I use the token to access protected resources
        Then the token should be accepted
        And I should be able to perform authorized operations
