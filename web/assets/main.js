
$(function() {
	
	// Create Map; default Münster Hafen or GetCurrentPosition
	var map = L.map('map').setView([51.95134, 7.64307], 15);

	L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    	maxZoom: 19,
    	attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
	}).addTo(map);

	// Load Data
	//$.get( "https://goldfish-app-yzovx.ondigitalocean.app/devices")
	$.get( "localhost:8000/devices")
	.done(function( data ) {
	   trackers = data
	   populateData(trackers, map);
	})
	.fail(function( data ) {
		trackers = dummyData();
		populateData(trackers, map);
	})
	.always(function( ) {
		$(".loader").remove();
	});

});

populateData = function(trackers, map) {

	// Populate map and tables
	for(var i=0; i < trackers.length; i++) {

		var tracker = trackers[i];

		var marker = L.marker([tracker.latitude, tracker.longitude]).addTo(map);

		$("#tracker-table").append(buildRow(tracker));
	}
	


	// fly to first marker
	if(trackers.length > 0) {

		map.flyTo([trackers[0].latitude, trackers[0].longitude])

	} else if (trackers.length < 1) {

		// if no trackers, try set current location and an example marker

		function getLocation() {
		  if (navigator.geolocation) {
		    navigator.geolocation.getCurrentPosition(function(position) {
		    	map.flyTo([position.coords.latitude, position.coords.longitude])
		    });
		  } else { 
		    // do nothing
		  }
		}

		// Set Hafen Marker
		var marker = L.marker([51.95134, 7.64307]).addTo(map);
	}
}

buildRow = function(trackerObj) {
	return "<tr><td>{id}</td><td>{owner_token}</td><td>{latitude}</td><td>{longitude}</td><td>{last_seen}</td><td>{shared_token}</td></tr>".format(trackerObj);
}

dummyData = function() {

	trackers = [
		{ id: 1, owner_token: "Max Fahrrad", latitude: 51.95153, longitude: 7.63805, last_seen: "gestern", shared_token: "Ja"},
		{ id: 2, owner_token: "Max Koffer", latitude: 51.95075, longitude: 7.63947, last_seen: "gestern", shared_token: "Ja"},
		{ id: 3, owner_token: "Max Rucksack", latitude: 51.94875, longitude: 7.63637, last_seen: "gestern", shared_token: "Nein"},
		{ id: 4, owner_token: "Nina Fahrrad ", latitude: 51.9531, longitude: 7.6425, last_seen: "gestern", shared_token: "Nein"},
		{ id: 5, owner_token: "Münster Akkuschrauber", latitude: 51.9560, longitude: 7.6353, last_seen: "gestern", shared_token: "Nein"},
		{ id: 6, owner_token: "Münster PKW", latitude: 51.94, longitude: 7.64207, last_seen: "gestern", shared_token: "Nein"},
	];

	return trackers;
}

// variadic arguments
String.prototype.format = function(dict) {
  var result = this;

  if(typeof(dict) === "object") {
    Object.keys(dict).forEach(function(key) {
      result = result.replace("{" + key + "}", dict[key]);
    });//from w ww . j a  va 2 s.  c o  m
    return result;
  }

  var args = [];
  var n = arguments.length;
  var i = 0;

  for(i; i < n; i+=1) {
    args.push(arguments[i]);
  }

  var result = this;

  args.forEach(function(arg) {
    result = result.replace("{}", arg);
  });

  return result;
}


