function postData() {
    fetch('https://ld-api.morganserver.com/insert_log', {
      method: 'POST',
    })
    .then(response => {
      if (response.ok) {
        console.log('Logs inserted into the database');
        location.reload();
      } else {
        console.error('Error inserting logs into the database');
        location.reload();
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
  }