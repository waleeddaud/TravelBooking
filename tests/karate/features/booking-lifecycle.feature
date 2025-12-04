Feature: Booking Lifecycle - Create, View, and Cancel Bookings

  Background:
    * url baseUrl
    * def uniqueEmail = 'bookinguser' + java.lang.System.currentTimeMillis() + '@example.com'
    * def password = 'BookingPass123!'

  Scenario: Complete Booking Flow - Flight Booking
    # Step 1: Register User
    Given path '/auth/register'
    And request { email: '#(uniqueEmail)', password: '#(password)', full_name: 'Booking Test User' }
    When method POST
    Then status 201
    
    # Step 2: Login and get token
    Given path '/auth/login'
    And form field username = uniqueEmail
    And form field password = password
    When method POST
    Then status 200
    And def authToken = response.access_token
    
    # Step 3: Search for flights
    Given path '/search/flights'
    And param origin = 'LHE'
    And param destination = 'DXB'
    When method GET
    Then status 200
    And match response[0].flight_id == '#notnull'
    And def flightId = response[0].flight_id
    
    # Step 4: Create booking
    Given path '/bookings'
    And header Authorization = 'Bearer ' + authToken
    And request { booking_type: 'flight', item_id: '#(flightId)', passengers: 2, special_requests: 'Window seat preferred' }
    When method POST
    Then status 201
    And match response.booking_id == '#notnull'
    And match response.status == 'pending'
    And match response.booking_type == 'flight'
    And match response.passengers == 2
    And def bookingId = response.booking_id
    
    # Step 5: Get booking details
    Given path '/bookings/' + bookingId
    And header Authorization = 'Bearer ' + authToken
    When method GET
    Then status 200
    And match response.booking_id == bookingId
    And match response.user_email == uniqueEmail
    
    # Step 6: Get user's booking history
    Given path '/users/me/bookings'
    And header Authorization = 'Bearer ' + authToken
    When method GET
    Then status 200
    And match response == '#[1]'
    And match response[0].booking_id == bookingId
    
    # Step 7: Cancel booking
    Given path '/bookings/' + bookingId + '/cancel'
    And header Authorization = 'Bearer ' + authToken
    When method PATCH
    Then status 200
    And match response.status == 'cancelled'

  Scenario: Create Booking - Unauthorized
    Given path '/bookings'
    And request { booking_type: 'flight', item_id: 'FL001', passengers: 1 }
    When method POST
    Then status 401

  Scenario: Create Booking - Invalid Flight ID
    # Register and login
    Given path '/auth/register'
    And request { email: '#(uniqueEmail)', password: '#(password)', full_name: 'Test User' }
    When method POST
    Then status 201
    
    Given path '/auth/login'
    And form field username = uniqueEmail
    And form field password = password
    When method POST
    Then status 200
    And def authToken = response.access_token
    
    # Try to book with invalid flight ID
    Given path '/bookings'
    And header Authorization = 'Bearer ' + authToken
    And request { booking_type: 'flight', item_id: 'INVALID_FLIGHT', passengers: 1 }
    When method POST
    Then status 400
    And match response.detail contains 'not found'

  Scenario: Get User Profile
    # Register and login
    Given path '/auth/register'
    And request { email: '#(uniqueEmail)', password: '#(password)', full_name: 'Profile Test User' }
    When method POST
    Then status 201
    
    Given path '/auth/login'
    And form field username = uniqueEmail
    And form field password = password
    When method POST
    Then status 200
    And def authToken = response.access_token
    
    # Get profile
    Given path '/users/me'
    And header Authorization = 'Bearer ' + authToken
    When method GET
    Then status 200
    And match response.email == uniqueEmail
    And match response.full_name == 'Profile Test User'
