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
      type: item.type
    };
  });

  return locations;
}

function initMap() {
  const map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 0, lng: 0 }, // Set the initial map center
    zoom: 2, // Set the initial zoom level
  });

  // Parse the JSON data and create markers for each location
  function createMarkers(data) {
    data.forEach((location) => {
      const marker = new google.maps.Marker({
        position: { lat: parseFloat(location.addr.lat), lng: parseFloat(location.addr.lng) },
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

  // Fetch the JSON data from the Django server
  function fetchMarkersData() {
    const locations = transformData('text': text,
    'first_name': first_name,
    'last_name': last_name,
    'nationality': nationality,
    'age': age,
    'gender': gender,
    'destinations': destinations,
    'duration': duration,
    'start_date': start_date,
     ); // Replace 'jsonData' with the actual JSON data
    return fetch('http://127.0.0.1:8000/bot/api/', {
      method: 'POST',
      headers: new Headers({
        'Authorization': 'bc8bf98f3bca1c5071d978b5192ef4c0c23837c85e1a42e5d03902d46d411894',
        'Content-Type': 'application/json',
      }),
<<<<<<< HEAD
      body: JSON.stringify(),
=======
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
>>>>>>> ae39520de81e60723ebcc9e93e1b80dfb86e8f6d
    })
      .then((response) => response.json())
      .then((data) => {
        //
      console.log(data);
      createMarkers(data);
    }).catch((error) => {
        console.error('Error:', error);
    });
  }

// Call fetchMarkersData() when the button is clicked
document.getElementById("TEST").addEventListener("click", fetchMarkersData);

fetchMarkersData(); // Call fetchMarkersData() on page load
}

// Call initMap() when the page finishes loading
window.onload = function () {
initMap();
};

