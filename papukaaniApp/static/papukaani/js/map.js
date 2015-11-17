function create_map( container, latlong, zoom){
    var map = new L.map(container, {zoomControl: false});
    var osm = L.tileLayer('http://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
        maxZoom: 16,
        attribution: 'Map data: &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'
    });
    map.addLayer(osm);
    map.setView(latlong, zoom);
    L.control.zoom({position: 'topright'}).addTo(map);

    return map;
}