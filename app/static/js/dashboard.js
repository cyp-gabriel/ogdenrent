document.addEventListener('DOMContentLoaded', () => {
  const deleteButtons = document.querySelectorAll('button.delete_button');
  deleteButtons.forEach((button) => {
    button.addEventListener('click', () => {
      onDelete(button.id);
    });
  });
});

document.addEventListener('DOMContentLoaded', () => {
  const deleteButtons = document.querySelectorAll('button.camera_button');
  deleteButtons.forEach((button) => {
    button.addEventListener('click', () => {
      onCamera(button.id);
    });
  });
});

function onDelete(id) {
  const numericString = id.match(/\d+$/)[0];
  const numericId = parseInt(numericString);

  $.ajax({
    url: `http://127.0.0.1:5000/api/v1/delete_customer/${numericId}`,
    type: 'DELETE',
    beforeSend: function(xhr) {
      xhr.setRequestHeader('Authorization', 'Basic ' + btoa('contact@boonecabal.co:Bogh0428$'));
    },
    success: function(response) {
      console.log(`Element with id ${numericId} was deleted`);
      location.reload();
    },
    error: function(xhr, status, error) {
      console.error(`Error: ${error}`);
    }
  });
}

function onCamera(id) {
  const numericString = id.match(/\d+$/)[0];
  const numericId = parseInt(numericString);

  $.ajax({
    url: `http://127.0.0.1:5000/api/v1/active_customer/${numericId}`,
    type: 'PUT',
    beforeSend: function(xhr) {
      xhr.setRequestHeader('Authorization', 'Basic ' + btoa('contact@boonecabal.co:Bogh0428$'));
    },
    success: function(response) {
      console.log(`Customer with id ${numericId} was made the active Customer, fiend.`);
      //location.reload();
    },
    error: function(xhr, status, error) {
      console.error(`Error: ${error}`);
    }
  });
}
