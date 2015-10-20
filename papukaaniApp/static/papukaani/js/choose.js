//Creates a map where the uploader can select the points which will be published.
function ChooseMap(points) {
    this.map = create_map("map", [61.0, 20.0], 5);

    this.markers = createEmptyMarkerClusterGroup();

    this.originalPoints = JSON.parse(JSON.stringify(points));

    this.points = points;

    this.createMarkersFromPoints(this.points, this.markers);
    this.map.addLayer(this.markers);
    this.showMarkersWithinTimeRange = this.showMarkersWithinTimeRange.bind(this)
}

//Updates the map to show all the markers within start and end, which are strings that Date.parse understands,
ChooseMap.prototype.showMarkersWithinTimeRange = function (start, end) {
    this.removeAllMarkers.call(this);
    pointsWithinRange = this.points.filter(function (point) {
        var timestring = point.timestamp.split(' ')[0];
        var timestamp = Date.parse(timestring);
        return timestamp >= Date.parse(start) && timestamp <= Date.parse(end)
    });
    this.createMarkersFromPoints(pointsWithinRange, this.markers);
    this.map.addLayer(this.markers);
};

//Creates an empty MarkerClusterGroup with initial settings.
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
    };

    clusterGroup = L.markerClusterGroup({
        zoomToBoundsOnClick: false,
        maxClusterRadius: 40,
        disableClusteringAtZoom: 13,
        singleMarkerMode: true,
        iconCreateFunction: customCluster
    });
    return clusterGroup
}

ChooseMap.prototype.changePoints = function(points){
    this.points = points;
    this.markers.clearLayers()

    this.createMarkersFromPoints(this.points, this.markers);
}


ChooseMap.prototype.removeAllMarkers = function () {
    this.map.removeLayer(this.markers);
    this.markers = createEmptyMarkerClusterGroup();
};


//Creates markers from point data and adds them to the marker cluster object.
ChooseMap.prototype.createMarkersFromPoints = function (points, markers) {
    for (var i = 0; i < points.length; i++) {
        var ltlgs = points[i].wgs84Geometry.coordinates;
        var marker = L.marker(new L.LatLng(ltlgs[0], ltlgs[1]));
        marker.pnt = points[i];
        marker.on('dblclick', this.changePublicity.bind(this, marker));

        markers.addLayer(marker);
    }
    clusterGroup.on('clusterdblclick', this.changeMarkerClusterPublicity.bind(this));
};

//Changes the publicity of every marker in marker cluster a.
ChooseMap.prototype.changeMarkerClusterPublicity = function (a) {
    var markers = a.layer.getAllChildMarkers();
    var changepublicityto = "public";
    if (getPublicChildCount(a.layer) > 0) {
        changepublicityto = "private";
    }

    for (var i = 0; i < markers.length; i++) {
        changePublicityTo(markers[i], changepublicityto);
        redrawIcon(markers[i]);
    }
    this.markers.refreshClusters(markers);
};

//Redraws the markers icon on the map.
redrawIcon = function (marker) {
    var c = ' marker-cluster';
    if (marker.pnt.public == true) c += '-small';
    else c += '-large';

    marker.setIcon(new L.DivIcon({
        html: '<div><span>' + (marker.pnt.public ? 1 : 0) + '/' + 1 + '</span></div>',
        className: 'marker-cluster' + c,
        iconSize: new L.Point(40, 40)
    }));
};

//Reverses the publicity of a marker and updates it.
ChooseMap.prototype.changePublicity = function (marker) {
    marker.pnt.publicity = (marker.pnt.publicity) === "public" ? "private" : "public";
    redrawIcon(marker);
    this.markers.refreshClusters(marker);
};

//Changes the publicity of a marker to the desired value.
changePublicityTo = function (marker, value) {
    marker.pnt.publicity = value;
};

//Counts the cluster's public child markers.
getPublicChildCount = function (cluster) {
    var pubcount = 0;

    var markers = cluster.getAllChildMarkers();
    for (var i = 0; i < markers.length; i++) {
        if (markers[i].pnt.publicity == "public") {
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
    request.send("data=" + encodeURIComponent(data));
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

function init(docs){
    documents = docs;
    devices = sortIntoDevices(documents);
    points = getAllPoints(devices);

    console.log(devices);
    console.log(points);

    map = new ChooseMap(points);
}

function getAllPoints(devices){
    var points = [];
    var device_keys = Object.keys(devices);
    for(i = 0; i < device_keys.length; i++){
        points = points.concat(devices[device_keys[i]]);
    }
    return points;
}

function changeDeviceSelection(deviceId){
    if(devices[deviceId]){
        points = devices[deviceId];
    } else {
        points = getAllPoints(devices);
    }

    map.changePoints(points)
}

//Resets the map to the state it was in when the page was loaded.
function resetMap(map) {
    map.map.removeLayer(map.markers);
    map.markers = createEmptyMarkerClusterGroup();
    map.points = JSON.parse(JSON.stringify(map.originalPoints));
    map.createMarkersFromPoints(map.points, map.markers);
    map.map.addLayer(map.markers);
    document.getElementById("start_time").value = "";
    document.getElementById("end_time").value = "";
}

function sortIntoDevices(documents){
    var devices = {};
    for(var i = 0; i < documents.length; i++){
        var deviceId = documents[i].deviceId;
        if(!devices[deviceId]){
            devices[deviceId] = [];
        }
        for(var j = 0; j < documents[i].gatherings.length; j++){
            devices[deviceId].push(documents[i].gatherings[j]);
        }
     }

     return devices;
}
