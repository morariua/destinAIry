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

// for testing: 


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
    }


// Call fetchMarkersData() when the button is clicked
document.getElementById("TEST").addEventListener("click", fetchMarkersData);

fetchMarkersData(); // Call fetchMarkersData() on page load
}

// Call initMap() when the page finishes loading
window.onload = function () {
initMap();
};

