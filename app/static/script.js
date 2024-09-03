function confirmSubmit(event) {
  let confirmed = confirm("Are you sure?")
  if (!confirmed) {
    event.preventDefault();
  }
}
