

function sendPostRequest(text, first_name, last_name, nationality, age, gender, destinations, duration, start_date) {
  fetch('http://127.0.0.1:8000/bot/api/', {
    method: 'POST',
    headers: new Headers({
      'Authorization': 'bc8bf98f3bca1c5071d978b5192ef4c0c23837c85e1a42e5d03902d46d411894',
      'Content-Type': 'application/json',
    }),
    body: JSON.stringify({
      'text': text,
      'first_name': first_name,
      'last_name': last_name,
      'nationality': nationality,
      'age': age,
      'gender': gender,
      'destinations': destinations,
      'duration': duration,
      'start_date': start_date,
    })
  })
    .then(response => response.json()) // Convert the response to JSON
    .then(result => {
      console.log(result);
      const data = result.data; // Extract the itinerary data from the response
      if (data && data.length > 0) {
        createMarkers(data); // Call createMarkers() with the itinerary data
      } else {
        console.error('No itinerary data returned from the AI.');
      }
    });
}

//Q: convert the values to json and then update the markers
//A: use JSON.stringify() to convert the values to JSON




// ...
// Call the sendPostRequest() function when the button is clicked

document.getElementById("LetsGoSub").addEventListener("click", function () {
    const duration = document.getElementById("start").value;
    const start = document.getElementById("date").value;
    const destinations = document.getElementById("destinations").value;
    const text = document.getElementById("extra").value;

    sendPostRequest(text, "Alex", "Morariu" , "romanian", "21", "male", destinations, duration, start);
});


const map = new ol.Map({
  target: 'map',
  layers: [
    new ol.layer.Tile({
      source: new ol.source.OSM()
    })
  ],
  view: new ol.View({
    center: ol.proj.fromLonLat([0, 0]), // Set the initial map center
    zoom: 2 // Set the initial zoom level
  })
});

const markers = [];

function createMarkers(data) {
  console.log(data.answer); // Check the value of data.answer

  const itineraryArray = JSON.parse(data.answer); // Parse the itinerary JSON array

  const features = []; // Array to hold the map features

  itineraryArray.forEach((location) => {
    const marker = new ol.Feature({
      geometry: new ol.geom.Point(ol.proj.fromLonLat([location.addr.lng, location.addr.lat])),
      name: location.name
    });

    const markerStyle = new ol.style.Style({
      image: new ol.style.Icon({
        src: 'path/to/marker-icon.png', // Replace with the path to your marker icon
        anchor: [0.5, 1]
      })
    });

    marker.setStyle(markerStyle);
    features.push(marker);
  });

  const vectorSource = new ol.source.Vector({
    features: features
  });

  const vectorLayer = new ol.layer.Vector({
    source: vectorSource
  });

  map.addLayer(vectorLayer);
}


