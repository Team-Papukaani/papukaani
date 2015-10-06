function ChooseMap(points){
    map = create_map("map", [61.0, 20.0], 5)

    this.blueIcon = L.icon({
        iconUrl: "/static/papukaani/media/blueMarker.png",
        iconSize: [38, 38],
        iconAnchor: [19, 38],
        popupAnchor: [-3, -76],
    });

    this.greyIcon = L.icon({
        iconUrl: "/static/papukaani/media/greyMarker.png",
        iconSize: [38, 38],
        iconAnchor: [19, 38],
        popupAnchor: [-3, -76],
    });

    this.markers = L.markerClusterGroup({
        zoomToBoundsOnClick: false,
        maxClusterRadius : 40,
        disableClusteringAtZoom : 13
    });

    this.markers.on('clusterdblclick', this.changeMarkerClusterPublicity.bind(this))
    this.points = points

    this.createMarkersFromPoints(this.points, this.markers)

    map.addLayer(this.markers);
};

//Creates markers from point data and adds them to the marker cluster object.
ChooseMap.prototype.createMarkersFromPoints = function(points, markers){
     for(var i = 0; i < points.length; i++){
        var ltlgs = points[i].latlong;
        var marker = L.marker(new L.LatLng(ltlgs[0],ltlgs[1]));
        marker.pnt = points[i];
        this.chooseIcon(marker);

        marker.on('dblclick', this.changePublicity.bind(this, marker));

        markers.addLayer(marker);
     }
};

//Changes the publicity of every marker in marker cluster a.
ChooseMap.prototype.changeMarkerClusterPublicity = function (a){
    var markers = a.layer.getAllChildMarkers()
    for(var i = 0; i < markers.length; i++){
        this.changePublicity(markers[i]);
    }
};


ChooseMap.prototype.chooseIcon = function (marker){
    icon = marker.pnt.public ? this.blueIcon : this.greyIcon;
    marker.setIcon(icon);
};

ChooseMap.prototype.changePublicity = function(marker){
    marker.pnt.public = !marker.pnt.public;
    this.chooseIcon(marker);
};

//Posts publicity data to server. Shows a message and disables the save button while waiting for response.
function send(csrf_token, points){
    data = JSON.stringify(points)
    messagebox = $("#loading");
    button = $("#save");

    messagebox.text("Tallennetaan...");
    button.attr("disabled", true);

    request = new XMLHttpRequest;

    request.onreadystatechange = function(){
        setLoadingMessage(request, button, messagebox)
    };

    request.open("POST","", true);
    set_headers(csrf_token, request);
    request.send("data="+data);
}

//Sets the content type and CSRF token cookie headers.
function set_headers(csrf_token, request){
    request.setRequestHeader("X-CSRFToken", csrf_token);
    request.setRequestHeader("Content-type","application/x-www-form-urlencoded");
}

//Callback function for post request. Shows a message depending on response status.
function setLoadingMessage(request, button, messagebox){
        if(request.readyState == 4){
            button.attr("disabled", false);
            if(request.status == 200){
                messagebox.text("Valmis!");
            } else{
                messagebox.text("Tapahtui virhe!");
            }
        }
    }