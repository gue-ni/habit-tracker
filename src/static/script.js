function createOccurence(id) {
  fetch( `create_occurence?id=${id}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': '{{ csrf_token() }}' // Include CSRF token if using Flask-WTF
    },
    body: JSON.stringify({ id: id })
  })
    .then(response => { console.log(response) })
    .catch(error => {
      console.error('Error:', error)
    });
}