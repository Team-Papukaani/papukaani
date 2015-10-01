function creatureMapInit(points){
    map = create_map("map", [61.0, 20.0], 5)

    var latlngs = createLatlngsFromPoints(points);


    // --- Arrow, with animation to demonstrate the use of setPatterns ---
    var arrow = L.polyline(latlngs, {color: 'blue', dashArray: '20,15'}).addTo(map);
    var arrowHead = L.polylineDecorator(arrow).addTo(map);

    var arrowOffset = 0;
    var anim = window.setInterval(function() {
        arrowHead.setPatterns([
            {offset: arrowOffset+'%', repeat: 0, symbol: L.Symbol.arrowHead({pixelSize: 15, polygon: false, pathOptions: {stroke: true}})}
        ])
        if(++arrowOffset > 100)
            arrowOffset = 0;
    }, 100);




//// --- Example with a rotated marker ---
//    var arrow = L.polyline(latlngs);
//    var pathPattern = L.polylineDecorator(
//        latlngs,
//        {
//            patterns: [
//                { offset: 0, repeat: 10, symbol: L.Symbol.dash({pixelSize: 5, pathOptions: {color: '#000', weight: 1, opacity: 0.2}}) },
//                { offset: '16%', repeat: '33%', symbol: L.Symbol.marker({rotate: true, markerOptions: {
//                    icon: L.icon({
//                        iconUrl: '/static/papukaani/libraries/polylinedecorator/icon_plane.png',
//                        iconAnchor: [16, 16]
//                    })
//                }})}
//            ]
//        }
//    ).addTo(map);



    // zoom the map to the polyline
    map.fitBounds(arrow.getBounds());
}

//Creates markers from point data and adds them to the marker cluster object.
function createLatlngsFromPoints(points){
    var latlngs = [];
    for(var i = 0; i < points.length; i++){
        var coordinates = points[i].latlong;
        var latlng = L.latLng(coordinates[0], coordinates[1]);
        latlngs.push(latlng);
    }
    return latlngs;
}