function init(data){
    points = JSON.parse(data); //Format : {latlong : [x,y], id : int}
    map = create_map("map", [61.0, 20.0], 5)

    latlongs = points.map(function(currentValue, index, array){
        return currentValue.latlong
    })

    if(latlongs){
        L.polyline(latlongs, {smoothFactor: 25.0}).addTo(map);
    }

    
}