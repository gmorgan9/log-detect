// var sunButton = document.getElementById('sunButton');
// var moonButton = document.getElementById('moonButton');
// var sun1 = document.getElementById('sun1');
// var moon = document.getElementById('moon');
// var graph = document.getElementById('graph');

// // sunButton.addEventListener('click', setLightTheme);
// // moonButton.addEventListener('click', setDarkTheme);

// sunButton.addEventListener('click', function() {
//     setLightTheme();
//     getBackgroundColor();
//   });
  
//   moonButton.addEventListener('click', function() {
//     setDarkTheme();
//     getBackgroundColor();
//   });


// function setLightTheme() {
//   var htmlElement = document.querySelector('html[data-bs-theme]');
//   htmlElement.dataset.bsTheme = 'light';
//   moon.classList.remove('hide');
//   moon.classList.add('active');
//   sun1.classList.add('hide');
//   sun1.classList.remove('active');
//   // graph.classList.remove('border1');
//   graph.classList.add('border');
// }
            
// function setDarkTheme() {
//   var htmlElement = document.querySelector('html[data-bs-theme]');
//   htmlElement.dataset.bsTheme = 'dark';
//   moon.classList.add('hide');
//   moon.classList.remove('active');
//   sun1.classList.remove('hide');
//   sun1.classList.add('active');
//   // graph.classList.remove('border');
//   graph.classList.add('border1');
// }


// // function getBackgroundColor() {
// //     var htmlElement = document.querySelector('html[data-bs-theme]');
// //     var currentTheme = htmlElement.dataset.bsTheme;
// //     var paperBgColor;
// //     console.log(currentTheme);
// //     if (currentTheme === 'dark') {
// //       // paperBgColor = '#2c3035';
// //       paperBgColor = '#222529';
// //       fontColor = '#aeb5bc';
// //     } else {
// //       paperBgColor = 'white';
// //       fontColor = '#515151';
// //     }



// function getBackgroundColor() {
//   var htmlElement = document.querySelector('html[data-bs-theme]');
//   var currentTheme = htmlElement.dataset.bsTheme;
//   var paperBgColor;
//   var fontColor;
  
//   // Make an HTTP GET request to your API endpoint
//   fetch('/api/data')
//     .then(response => response.json())
//     .then(data => {
//       // Assuming the API response is an array of user objects
//       var user = data[0]; // Assuming you want the mode of the first user in the response

//       // Assuming the user object has a 'mode' property
//       var userMode = user.mode;
      
//       console.log("userMode");
//       if (userMode === 1) {
//         paperBgColor = 'dark';
//         fontColor = '#aeb5bc';
//       } else if (userMode === 2) {
//         paperBgColor = 'light';
//         fontColor = '#515151';
//       } else {
//         // Default theme if the user's mode is not recognized
//         paperBgColor = 'light';
//         fontColor = '#515151';
//       }

//       if (currentTheme !== paperBgColor) {
//         // Change the theme only if it's different from the user's preference
//         htmlElement.dataset.bsTheme = paperBgColor;
//       }

//       // Rest of your code...
//     })
//     .catch(error => {
//       console.error('Error:', error);
//     });







  
//     // Update the graph's background color
//     var layout = {
//       xaxis: { title: "<span style='font-weight: bold; color: " + fontColor + "'>Total Alerts:</span> <span style='color: " + fontColor + "'> " + total + "</span>", tickfont: { color: fontColor } },
//       yaxis: { tickfont: { color: fontColor } },
//       title: "<span style='color: " + fontColor + "'>Weekly Alert Total</span><br>" + "<span style='font-size: 12px;color: " + fontColor + "'>" + sun + " - " + sat + "</span>",
//       paper_bgcolor: paperBgColor,
//       plot_bgcolor: paperBgColor
//     };
  
//     Plotly.react('barGraph', data, layout);
//   }

var sunButton = document.getElementById('sunButton');
var moonButton = document.getElementById('moonButton');
var sun1 = document.getElementById('sun1');
var moon = document.getElementById('moon');
var graph = document.getElementById('graph');



sunButton.addEventListener('click', function() {
  setLightTheme();
  getBackgroundColor();
});

moonButton.addEventListener('click', function() {
  setDarkTheme();
  getBackgroundColor();
});

document.addEventListener('DOMContentLoaded', function() {
  getBackgroundColor();
});

function setLightTheme() {
  var htmlElement = document.querySelector('html[data-bs-theme]');
  htmlElement.dataset.bsTheme = 'light';
  moon.classList.remove('hide');
  moon.classList.add('active');
  sun1.classList.add('hide');
  sun1.classList.remove('active');
  // graph.classList.remove('border1');
  graph.classList.add('border');
}

function setDarkTheme() {
  var htmlElement = document.querySelector('html[data-bs-theme]');
  htmlElement.dataset.bsTheme = 'dark';
  moon.classList.add('hide');
  moon.classList.remove('active');
  sun1.classList.remove('hide');
  sun1.classList.add('active');
  // graph.classList.remove('border');
  graph.classList.add('border1');
}

function getBackgroundColor() {
  var htmlElement = document.querySelector('html[data-bs-theme]');
  var currentTheme = htmlElement.dataset.bsTheme;
  var paperBgColor;
  var fontColor;

  // Make an HTTP GET request to your API endpoint
fetch('https://ld-api.morganserver.com/api/data')
.then(response => response.json())
.then(data => {
  // Assuming the API response is an array of user objects
  // var user = data[0]; // Assuming you want the mode of the first user in the response

  // Assuming the user object has a 'mode' property
  var userMode = data.mode;

  console.log(userMode);
  if (userMode === 1) {
    paperBgColor = 'dark';
    fontColor = '#aeb5bc';
  } else if (userMode === 2) {
    paperBgColor = 'light';
    fontColor = '#515151';
  } else {
    // Default theme if the user's mode is not recognized
    paperBgColor = 'light';
    fontColor = '#515151';
  }

  if (currentTheme !== paperBgColor) {
    // Change the theme only if it's different from the user's preference
    htmlElement.dataset.bsTheme = paperBgColor;
  }

  // Rest of your code...
  updateGraphColors(paperBgColor, fontColor);
})
.catch(error => {
  console.error('Error:', error);
});
}

function updateGraphColors(paperBgColor, fontColor) {
  // Update the graph's background color
  var layout = {
    xaxis: { title: "<span style='font-weight: bold; color: " + fontColor + "'>Total Alerts:</span> <span style='color: " + fontColor + "'> " + total + "</span>", tickfont: { color: fontColor } },
    yaxis: { tickfont: { color: fontColor } },
    title: "<span style='color: " + fontColor + "'>Weekly Alert Total</span><br>" + "<span style='font-size: 12px;color: " + fontColor + "'>" + sun + " - " + sat + "</span>",
    paper_bgcolor: paperBgColor,
    plot_bgcolor: paperBgColor
  };

  Plotly.react('barGraph', data, layout);
}
