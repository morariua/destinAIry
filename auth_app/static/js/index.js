const markers = [];

function transformData(data) {
  const locations = data.map((item) => {
    // Customize this logic to extract the required fields from 'item'
    return {
      date: item.date,
      name: item.name,
      addr: item.addr,
      pop: item.pop,
      hrs: item.hrs,
      mode: item.mode,
      cost: item.cost,
      remark: item.remark,
      type: item.type,
    };
  });

  return locations;
}

function initMap() {
  const map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 0, lng: 0 }, // Set the initial map center
    zoom: 2, // Set the initial zoom level
  });
  const directionsService = new google.maps.DirectionsService();

  // Parse the JSON file and create markers for each location
  function createMarkers(locations) {
    locations.forEach((location) => {
      const marker = new google.maps.Marker({
        position: { lat: parseFloat(location.latitude), lng: parseFloat(location.longitude) },
        map: map,
        title: location.name,
        optimized: true,
      });

      // Create an info window to display the location details
      const infoWindow = new google.maps.InfoWindow({
        content: `
          <div>
            <h3>${location.name}</h3>
            <p>Date: ${location.date}</p>
            <p>Address: ${location.addr}</p>
            <p>Population: ${location.pop}</p>
            <p>Hours: ${location.hrs}</p>
            <p>Mode: ${location.mode}</p>
            <p>Cost: ${location.cost}</p>
            <p>Remark: ${location.remark}</p>
            <p>Type: ${location.type}</p>
          </div>
        `,
      });

      // Show the info window when the marker is clicked
      marker.addListener("click", () => {
        infoWindow.open(map, marker);
      });

      markers.push(marker);
    });
  }

  // Fetch the JSON data from the Django server based on user question
  function fetchMarkersData(question) {
    return fetch('http://127.0.0.1:8000/bot/api/', {
      method: 'POST',
      headers: new Headers({
        'Authorization': 'bc8bf98f3bca1c5071d978b5192ef4c0c23837c85e1a42e5d03902d46d411894',
        'Content-Type': 'application/json',
      }),
      body: { 'text': text,
        'first_name': first_name,
        'last_name': last_name,
        'nationality': nationality,
        'age': age,
        'gender': gender,
        'destinations': destinations,
        'duration': duration,
        'start_date': start_date,
         },
    })
      .then((response) => response.json())
      .then((data) => {
        // Process the JSON data and create markers on the map
        console.log(data);
        const locations = transformData(data);
        createMarkers(locations);
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  }

  // Call fetchMarkersData() on page load with a sample question
  fetchMarkersData('Hello'); // Replace 'Hello' with the desired user question

  // Optional: Call fetchMarkersData() when a button with id "TEST" is clicked
  document.getElementById("TEST").addEventListener("click", () => {
    const userQuestion = prompt("Enter your question:");
    if (userQuestion) {
      fetchMarkersData(userQuestion);
    }
  });
}

// Call initMap() when the page finishes loading
window.onload = function () {
  initMap();
};
