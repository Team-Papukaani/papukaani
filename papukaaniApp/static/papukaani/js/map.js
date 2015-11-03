function create_map( container, latlong, zoom){
    var map = new L.map(container, {zoomControl: false});
    var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
    var osmAttrib = 'Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
    var osm = new L.TileLayer(osmUrl, {attribution: osmAttrib});
    map.addLayer(osm);
    map.setView(latlong, zoom);
    L.control.zoom({position: 'topright'}).addTo(map);

    return map;
}