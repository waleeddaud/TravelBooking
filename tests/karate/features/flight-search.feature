Feature: Flight Search

  Background:
    * url baseUrl

  Scenario: Search Flights - Valid Route
    Given path '/search/flights'
    And param origin = 'LHE'
    And param destination = 'DXB'
    When method GET
    Then status 200
    And match response == '#[]'
    And match each response contains { flight_id: '#string', airline: '#string', origin: 'LHE', destination: 'DXB' }

  Scenario: Search Flights - Valid Route LHE to LHR
    Given path '/search/flights'
    And param origin = 'LHE'
    And param destination = 'LHR'
    When method GET
    Then status 200
    And match response == '#[]'
    And match each response contains { origin: 'LHE', destination: 'LHR' }

  Scenario: Search Flights - No Results
    Given path '/search/flights'
    And param origin = 'XYZ'
    And param destination = 'ABC'
    When method GET
    Then status 200
    And match response == []

  Scenario: Search Hotels - Valid City
    Given path '/search/hotels'
    And param city = 'Dubai'
    When method GET
    Then status 200
    And match response == '#[]'
    And match each response contains { hotel_id: '#string', name: '#string', city: 'Dubai' }

  Scenario: Search Hotels - No Results
    Given path '/search/hotels'
    And param city = 'NonexistentCity'
    When method GET
    Then status 200
    And match response == []
