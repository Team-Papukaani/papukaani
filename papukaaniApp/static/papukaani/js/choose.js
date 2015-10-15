//Creates a map where the uploader can select the points which will be published.
function ChooseMap(points) {
    this.map = create_map("map", [61.0, 20.0], 5)

    this.markers = createEmptyMarkerClusterGroup();

    this.points = points

    this.createMarkersFromPoints(this.points, this.markers)
    this.map.addLayer(this.markers)
    this.showMarkersWithinTimeRange = this.showMarkersWithinTimeRange.bind(this)
};

//Updates the map to show all the markers within start and end, which are strings that Date.parse understands,
ChooseMap.prototype.showMarkersWithinTimeRange = function(start, end) {
    this.removeAllMarkers.call(this)
    pointsWithinRange = this.points.filter(function(point) {
        timestamp = Date.parse(point.timestamp)
        return timestamp >= Date.parse(start) && timestamp <= Date.parse(end)
    });
    this.createMarkersFromPoints(pointsWithinRange, this.markers)
    this.map.addLayer(this.markers)
}

//
function createEmptyMarkerClusterGroup() {
    customCluster = function (cluster) {
        var childCount = cluster.getChildCount();
        var pubcount = getPublicChildCount(cluster);

        var c = ' marker-cluster';
        if (pubcount === 0) c += '-large';
        else if (pubcount < childCount) c += '-medium';
        else c += '-small';

        return new L.DivIcon({
            html: '<div><span>' + pubcount + "/" + childCount + '</span></div>',
            className: 'marker-cluster' + c,
            iconSize: new L.Point(40, 40)
        });
    }

    clusterGroup = L.markerClusterGroup({
        zoomToBoundsOnClick: false,
        maxClusterRadius: 40,
        disableClusteringAtZoom: 13,
        singleMarkerMode: true,
        iconCreateFunction: customCluster
    });
    return clusterGroup
}
ChooseMap.prototype.removeAllMarkers = function() {
    this.map.removeLayer(this.markers)
    this.markers = createEmptyMarkerClusterGroup();
}

//Creates markers from point data and adds them to the marker cluster object.
ChooseMap.prototype.createMarkersFromPoints = function (points, markers) {
    for (var i = 0; i < points.length - 10; i++) {
        var ltlgs = points[i].latlong;
        var marker = L.marker(new L.LatLng(ltlgs[0], ltlgs[1]));
        marker.pnt = points[i];
        marker.on('dblclick', this.changePublicity.bind(this, marker));

        markers.addLayer(marker);
    }
    clusterGroup.on('clusterdblclick', this.changeMarkerClusterPublicity.bind(this));
};

//Changes the publicity of every marker in marker cluster a.
ChooseMap.prototype.changeMarkerClusterPublicity = function (a) {
    console.log("function called");
    var markers = a.layer.getAllChildMarkers();
    var changepublicityto = true;
    if (getPublicChildCount(a.layer) > 0) {
        changepublicityto = false;
    }

    for (var i = 0; i < markers.length; i++) {
        changePublicityTo(markers[i], changepublicityto);
        this.markers.removeLayer(markers[i]);
        this.markers.addLayer(markers[i]);
    }
};

ChooseMap.prototype.changePublicity = function (marker) {
    marker.pnt.public = !marker.pnt.public;
    this.markers.removeLayer(marker);
    this.markers.addLayer(marker);
};

changePublicityTo = function (marker, value) {
    marker.pnt.public = value;
};

getPublicChildCount = function (cluster) {
    var pubcount = 0;

    var markers = cluster.getAllChildMarkers()
    for (var i = 0; i < markers.length; i++) {
        if (markers[i].pnt.public) {
            pubcount++;
        }
    }
    return pubcount;
};

//Posts publicity data to server. Shows a message and disables the save button while waiting for response.
function send(csrf_token, points) {
    data = JSON.stringify(points);
    messagebox = $("#loading");
    button = $("#save");

    messagebox.text("Tallennetaan...");
    button.attr("disabled", true);

    request = new XMLHttpRequest;

    request.onreadystatechange = function () {
        setLoadingMessage(request, button, messagebox)
    };

    request.open("POST", "", true);
    set_headers(csrf_token, request);
    request.send("data=" + data);
}

//Sets the content type and CSRF token cookie headers.
function set_headers(csrf_token, request) {
    request.setRequestHeader("X-CSRFToken", csrf_token);
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
}

//Callback function for post request. Shows a message depending on response status.
function setLoadingMessage(request, button, messagebox) {
    if (request.readyState == 4) {
        button.attr("disabled", false);
        if (request.status == 200) {
            messagebox.text("Valmis!");
        } else {
            messagebox.text("Tapahtui virhe!");
        }
    }
}
