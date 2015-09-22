function init(data){
    points = JSON.parse(data); //Format : {latlong : [x,y], id : int}
    map = create_map("map", [61.0, 20.0], 5)

    markers = L.markerClusterGroup({zoomToBoundsOnClick: false});

    markers.on('clusterdblclick', function(a){
        var mkrs = a.layer.getAllChildMarkers()
        for(var i = 0; i < mkrs.length; i++){
            mkrs[i].pnt.public = !mkrs[i].pnt.public;
        }
    })

    for(var i = 0; i < points.length; i++){
        var ltlgs = points[i].latlong;
        var marker = L.marker(new L.LatLng(ltlgs[0],ltlgs[1]));
        marker.pnt = points[i]

        marker.on('dblclick', function(p){
            return function(e){
                p.public = !p.public;
            }
        }(points[i]));

        markers.addLayer(marker);
    }

    map.addLayer(markers)
}



