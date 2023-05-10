/**
 * This function adds a click event listener to a button with the given customer ID.
 *
 * @param {string} customerId - The ID of the button to add the click event listener to.
 */
function btnSubmit(customerId) {
  console.log(customerID);
  $(customerId).click(function() {
    $.ajax({
      url: '/new_application',
      method: 'POST',
      success: function(data) {
        console.log(response);
      }
    });
  });

  /*
  var c = document.getElementById(customerId);
  $(customerId).click(function() {
    $.ajax({
      url: '/dashboard',
      method: 'GET',
      success: function(data) {
        
      }
    })
  });
  */
}