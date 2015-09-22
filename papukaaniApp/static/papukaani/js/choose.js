function init(data){
    points = JSON.parse(data); //Format : {latlong : [x,y], id : int}
    map = create_map("map", [61.0, 20.0], 5)

     blueIcon = L.icon({
        iconUrl: "/static/papukaani/media/blueMarker.png",
        iconSize: [38, 38],
        iconAnchor: [19, 38],
        popupAnchor: [-3, -76],
     });

     greyIcon = L.icon({
        iconUrl: "/static/papukaani/media/greyMarker.png",
        iconSize: [38, 38],
        iconAnchor: [19, 38],
        popupAnchor: [-3, -76],
     });



    markers = L.markerClusterGroup({
        zoomToBoundsOnClick: false,
        maxClusterRadius : 40,
        disableClusteringAtZoom : 13
    });

    markers.on('clusterdblclick', function(a){
        var mkrs = a.layer.getAllChildMarkers()
        for(var i = 0; i < mkrs.length; i++){
            changePublicity(mkrs[i]);
        }
    })

    for(var i = 0; i < points.length; i++){
        var ltlgs = points[i].latlong;
        var marker = L.marker(new L.LatLng(ltlgs[0],ltlgs[1]));
        marker.pnt = points[i];
        chooseIcon(marker);

        marker.on('dblclick', function(marker){
            return function(e){
                changePublicity(marker);
            }
        }(marker));

        markers.addLayer(marker);
    }

    map.addLayer(markers);
}

function chooseIcon(marker){
    icon = marker.pnt.public ? blueIcon : greyIcon;
    marker.setIcon(icon);
}

function changePublicity(marker){
    marker.pnt.public = !marker.pnt.public;
    chooseIcon(marker);
}

function send(csrf_token){
    data = JSON.stringify(points)
    xmlhttp = new XMLHttpRequest;

    xmlhttp.open("POST","", true);
    xmlhttp.setRequestHeader("X-CSRFToken", csrf_token);
    xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xmlhttp.send("data="+data);
}
