var sunButton = document.getElementById('sunButton');
var moonButton = document.getElementById('moonButton');
var sun1 = document.getElementById('sun1');
var moon = document.getElementById('moon');
var graph = document.getElementById('graph');

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

  

fetch('https://ld-api.morganserver.com/api/data')
  .then(response => response.json())
  .then(data => {
    var user = data[0];
    var userMode = user.mode;

    var htmlElement = document.querySelector('html[data-bs-theme]');
  var currentTheme = htmlElement.dataset.bsTheme;
  var paperBgColor;
  var fontColor;
    console.log(userMode);
    if (userMode === 1) {
      // User mode is 1
      console.log("dark");
      paperBgColor = 'dark';
      fontColor = '#aeb5bc';
    } else if (userMode === 2) {
      // User mode is 2
      console.log("light");
      paperBgColor = 'light';
      fontColor = '#515151';
    } else {
      // User mode is neither 1 nor 2
      console.log("nothing");
    }
    if (currentTheme !== paperBgColor) {
        // Change the theme only if it's different from the user's preference
        htmlElement.dataset.bsTheme = paperBgColor;
      }
    updateGraphColors(paperBgColor, fontColor);
  })
  .catch(error => {
    console.error('Error:', error);
  });

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

  