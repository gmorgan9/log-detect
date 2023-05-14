function postData() {
    fetch('https://ld-api.morganserver.com/insert_alert', {
      method: 'POST',
    })
    .then(response => {
      if (response.ok) {
        console.log('Alerts inserted into the database');
        location.reload();
      } else {
        console.error('Error inserting alerts into the database');
        location.reload();
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
  }