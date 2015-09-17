
create_map_with_points = function(points) {
    var map = L.map('map');
    var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
    var osmAttrib = 'Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
    var osm = new L.TileLayer(osmUrl, {attribution: osmAttrib});
    map.addLayer(osm);
    map.setView([61.0, 20.0], 5);

    if(points){
        L.polyline(points, {smoothFactor: 25.0}).addTo(map);
    }

}