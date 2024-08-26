function createOccurence(id) {
  fetch(`create_occurence?id=${id}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': '{{ csrf_token() }}'
    },
    body: JSON.stringify({ id: id })
  })
    .then(response => { console.log(response) })
    .catch(error => {
      console.error('Error:', error)
    });
}

function createMeasurement(id) {
  const input = window.prompt("Input Number:", "0.0");
  const number = parseFloat(input);
  console.log(number)

  fetch(`create_measurement?id=${id}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': '{{ csrf_token() }}'
    },
    body: JSON.stringify({ id: id, value: number })
  })
    .then(response => { console.log(response) })
    .catch(error => {
      console.error('Error:', error)
    });
}