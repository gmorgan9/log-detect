// fetch('https://ld-api.morganserver.com/api/data')
//   .then(response => response.json())
//   .then(data => {
//     var user = data[0];
//     var userMode = user.mode;

//     console.log(userMode);
//     if (userMode === 1) {
//       // User mode is 1
//       console.log("dark");
//     } else if (userMode === 2) {
//       // User mode is 2
//       console.log("light");
//     } else {
//       // User mode is neither 1 nor 2
//       console.log("nothing");
//     }
//   })
//   .catch(error => {
//     console.error('Error:', error);
//   });

// var sunButton = document.getElementById('sunButton');
// var moonButton = document.getElementById('moonButton');
// var sun1 = document.getElementById('sun1');
// var moon = document.getElementById('moon');
// var graph = document.getElementById('graph');



// sunButton.addEventListener('click', function() {
//   setLightTheme();
//   getBackgroundColor();
// });

// moonButton.addEventListener('click', function() {
//   setDarkTheme();
//   getBackgroundColor();
// });





// function getBackgroundColor() {
  

//   // Make an HTTP GET request to your API endpoint
// fetch('https://ld-api.morganserver.com/api/data')
// .then(response => response.json())
// .then(data => {
//   // Assuming the API response is an array of user objects
//   // var user = data[0]; // Assuming you want the mode of the first user in the response

//   // Assuming the user object has a 'mode' property
//   var userMode = data.mode;

//   console.log(userMode);
//   if (userMode === 1) {
//     paperBgColor = 'dark';
//     fontColor = '#aeb5bc';
//   } else if (userMode === 2) {
//     paperBgColor = 'light';
//     fontColor = '#515151';
//   } else {
//     // Default theme if the user's mode is not recognized
//     paperBgColor = 'light';
//     fontColor = '#515151';
//   }

//   if (currentTheme !== paperBgColor) {
//     // Change the theme only if it's different from the user's preference
//     htmlElement.dataset.bsTheme = paperBgColor;
//   }

//   // Rest of your code...
//   updateGraphColors(paperBgColor, fontColor);
// })
// .catch(error => {
//   console.error('Error:', error);
// });
// }


