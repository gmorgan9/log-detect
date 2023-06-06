fetch('https://ld-api.morganserver.com/api/data')
  .then(response => response.json())
  .then(data => {
    var user = data[0];
    var userMode = user.mode;

    console.log(userMode);
    if (userMode === 1) {
      // User mode is 1
      console.log("dark");
    } else if (userMode === 2) {
      // User mode is 2
      console.log("light");
    } else {
      // User mode is neither 1 nor 2
      console.log("nothing");
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });