function postData() {
    fetch('https://ld-api.morganserver.com/insert_alert', {
      method: 'POST',
    })
    .then(response => {
      if (response.ok) {
        // Handle successful response
        console.log('Alerts inserted into the database');
        location.reload(); // Reload the page
      } else {
        // Handle error response
        console.error('Error inserting alerts into the database');
      }
    })
    .catch(error => {
      // Handle fetch error
      console.error('Error:', error);
    });
  }