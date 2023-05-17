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
  fetch(`http://127.0.0.1:5000/api/v1/delete_customer/${numericId}`, {
    method: 'DELETE',
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    // delete the element with the corresponding id
    console.log(`Element with id ${numericId} was deleted`);
  })
  .catch(error => {
    console.error('There was a problem with the fetch operation:', error);
  });
}
