// Load the map and directions service
function initMap() {
    const map = new google.maps.Map(document.getElementById("map"), {
      center: { lat: 0, lng: 0 }, // Set the initial map center
      zoom: 2, // Set the initial zoom level
    });
    const directionsService = new google.maps.DirectionsService();
  
    // Parse the JSON file and create markers for each location
    const locations = JSON.parse(jsonFile); // Replace 'jsonFile' with the variable containing your JSON data
    const markers = [];
  
    locations.forEach((location) => {
      const marker = new google.maps.Marker({
        position: { lat: location.latitude, lng: location.longitude },
        map: map,
        title: location.name,
      });
      markers.push(marker);
    });
  
    // Request directions and travel distances between locations with different travel modes
    const travelModes = [
      google.maps.TravelMode.DRIVING,
      google.maps.TravelMode.WALKING,
      google.maps.TravelMode.BICYCLING,
      google.maps.TravelMode.TRANSIT,
    ];
  
    for (let i = 0; i < markers.length - 1; i++) {
      const origin = markers[i].position;
      const destination = markers[i + 1].position;
  
      travelModes.forEach((mode) => {
        const request = {
          origin: origin,
          destination: destination,
          travelMode: mode,
        };
  
        directionsService.route(request, function (result, status) {
          if (status === google.maps.DirectionsStatus.OK) {
            const distance = result.routes[0].legs[0].distance.text;
            console.log(`Distance from ${locations[i].name} to ${locations[i + 1].name} (${mode}): ${distance}`);
          }
        });
      });
    }
  }

  window.onload = function() {
    initMap();
  }