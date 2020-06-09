// leaflet map
if (typeof customLat !== 'undefined') {
    var setViewLat = 35.7785733;
} else {
    var setViewLat = customLat;
}

if (typeof customLon !== 'undefined') {
    var setViewLon = -78.6395438;
} else {
    var setViewLon = customLon;
}

var map = L.map('map', {fullscreenControl: true}).setView([setViewLat,setViewLon], 6);

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
    maxZoom: 18,
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
        '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
        'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1
}).addTo(map);

var markerClusters = L.markerClusterGroup();

// Add video to markerClusters
for (var i = 0; i < video_map_data.length; ++i){
  var popup = video_map_data[i].fields.name + " [<a href=\"/map/video/" + video_map_data[i].pk + "\">🎥</a>]";

  var m = L.marker([video_map_data[i].fields.lat, video_map_data[i].fields.lon])
                  .bindPopup(popup);

  markerClusters.addLayer(m);
}

// Add vr to markerClusters
for (var i = 0; i < vr_map_data.length; ++i){
  var popup = vr_map_data[i].fields.name + " [<a href=\"/map/vr/" + vr_map_data[i].pk + "\">🎥</a>]";

  var m = L.marker([vr_map_data[i].fields.lat, vr_map_data[i].fields.lon])
                  .bindPopup(popup);

  markerClusters.addLayer(m);
}

// Add externals to markerClusters
for (var i = 0; i < external_map_data.length; ++i){
  var popup = external_map_data[i].fields.name + " [<a href=\"/map/external/" + external_map_data[i].pk + "\">🎥</a>]";

  var m = L.marker([external_map_data[i].fields.lat, external_map_data[i].fields.lon])
                  .bindPopup(popup);

  markerClusters.addLayer(m);
}

map.addLayer(markerClusters);