Feature: Authentication - User Registration and Login

  Background:
    * url baseUrl
    * def uniqueEmail = 'testuser' + java.lang.System.currentTimeMillis() + '@example.com'

  Scenario: User Registration - Success
    Given path '/auth/register'
    And request { email: '#(uniqueEmail)', password: 'TestPassword123!', full_name: 'Test User' }
    When method POST
    Then status 201
    And match response.email == uniqueEmail
    And match response.full_name == 'Test User'
    And match response.is_active == true

  Scenario: User Registration - Duplicate Email
    Given path '/auth/register'
    And request { email: '#(uniqueEmail)', password: 'TestPassword123!', full_name: 'Test User' }
    When method POST
    Then status 201
    
    # Try to register again with same email
    Given path '/auth/register'
    And request { email: '#(uniqueEmail)', password: 'DifferentPass456!', full_name: 'Another User' }
    When method POST
    Then status 400
    And match response.detail contains 'already registered'

  Scenario: User Login - Success
    # First register a user
    Given path '/auth/register'
    And request { email: '#(uniqueEmail)', password: 'TestPassword123!', full_name: 'Test User' }
    When method POST
    Then status 201
    
    # Then login
    Given path '/auth/login'
    And form field username = uniqueEmail
    And form field password = 'TestPassword123!'
    When method POST
    Then status 200
    And match response.access_token == '#notnull'
    And match response.token_type == 'bearer'

  Scenario: User Login - Invalid Credentials
    Given path '/auth/login'
    And form field username = 'nonexistent@example.com'
    And form field password = 'WrongPassword'
    When method POST
    Then status 401
    And match response.detail contains 'Incorrect'
