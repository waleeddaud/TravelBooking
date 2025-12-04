Feature: Mock Payment Service

  # This feature file simulates a payment gateway for testing purposes
  # In production, this would be replaced with actual payment provider integration

  Background:
    * def paymentResponse = 
      """
      function(amount) {
        if (amount <= 0) {
          return { success: false, message: 'Invalid amount', transaction_id: null };
        }
        return { 
          success: true, 
          message: 'Payment processed successfully', 
          transaction_id: 'TXN' + java.lang.System.currentTimeMillis() 
        };
      }
      """

  Scenario: Mock Payment - Success
    * def amount = 500.00
    * def result = paymentResponse(amount)
    * match result.success == true
    * match result.transaction_id == '#notnull'

  Scenario: Mock Payment - Invalid Amount
    * def amount = -100.00
    * def result = paymentResponse(amount)
    * match result.success == false
    * match result.transaction_id == null
