
create_map_with_points = function(data) {
    points = JSON.parse(data)
    map = create_map("map", [61.0, 20.0], 5)

    if(points){
        L.polyline(points, {smoothFactor: 25.0}).addTo(map);
    }

}