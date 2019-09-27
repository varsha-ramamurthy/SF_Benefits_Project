// API key
const API_KEY = "pk.eyJ1IjoidmFyc2hhLXJhbWFtdXJ0aHkiLCJhIjoiY2swOW1oOGc1MGE4bDNtcmxrdWF6ZDJtNiJ9.CVgyBAclrEtqRhOXaVPgug";

// Create a map object
var myMap = L.map("map", {
    center: [37.09, -95.71],
    zoom: 5
  });
  
  L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 18,
    id: "mapbox.streets-basic",
    accessToken: API_KEY
  }).addTo(myMap);
  
  // Define a markerSize function that will give the city a different radius based on its size
  function markerSize(size) {
    return size*1000;
  }
  
  
  // Create San Francisco dictionary
  
   var sf_data = {
      name: "San Francisco",
      location: [37.774929, -122.419418],
      population: 884363,
      size: 46.87
    };
  
    L.circle(sf_data.location, {
      fillOpacity: 0.75,
      color: "black",
      fillColor: "blue",
      // Setting our circle's radius equal to the output of our markerSize function
      // This will make our marker's size proportionate to its population
      radius: markerSize(sf_data.size)
    }).bindPopup("<h1>" + sf_data.name + "</h1> <hr> <h2>Population: " + sf_data.population + "</h2> <hr> <h3>Area: " + sf_data.size + " sq. mi</h3>").addTo(myMap);
  