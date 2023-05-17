document.addEventListener('DOMContentLoaded', () => {
  const deleteButtons = document.querySelectorAll('button.delete_button');
  deleteButtons.forEach((button) => {
    button.addEventListener('click', () => {
      onDelete(button.id);
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
      xhr.setRequestHeader('Authorization', 'Basic ' + btoa('boone.cabal@gmail.com:grantaster'));
    },
    success: function(response) {
      console.log(`Element with id ${numericId} was deleted`);
      location.reload();
    }
  });
}
