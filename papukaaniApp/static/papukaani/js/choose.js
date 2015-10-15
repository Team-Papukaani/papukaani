//Creates a map where the uploader can select the points which will be published.
function ChooseMap(points) {
    this.map = create_map("map", [61.0, 20.0], 5)

    this.markers = L.markerClusterGroup({
        zoomToBoundsOnClick: false,
        maxClusterRadius: 40,
        disableClusteringAtZoom: 13,
        singleMarkerMode: true,
        iconCreateFunction: this.customCluster
    });

    this.markers.on('clusterdblclick', this.changeMarkerClusterPublicity.bind(this));
    this.points = points;

    this.createMarkersFromPoints(this.points, this.markers);

    this.map.addLayer(this.markers);
}
ChooseMap.prototype.changePoints = function(points){
    this.points = points;
    this.markers.clearLayers()

    this.createMarkersFromPoints(this.points, this.markers);
}


//Creates markers from point data and adds them to the marker cluster object.
ChooseMap.prototype.createMarkersFromPoints = function (points, markers) {
    for (var i = 0; i < points.length; i++) {
        var ltlgs = points[i].wgs84Geometry.coordinates;
        var marker = L.marker(new L.LatLng(ltlgs[0], ltlgs[1]));
        marker.pnt = points[i];
        marker.on('dblclick', this.changePublicity.bind(this, marker));

        markers.addLayer(marker);
    }
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
    }
    this.markers.refreshClusters(markers);
};

//Reverses the publicity of a marker and updates it.
ChooseMap.prototype.changePublicity = function (marker) {
    marker.pnt.publicity = (marker.pnt.publicity) === "public" ? "private" : "public";
    this.markers.refreshClusters(marker);
};

//Changes the publicity of a marker to the desired value.
changePublicityTo = function (marker, value) {
    marker.pnt.publicity = value;
};

//Custom function for MarkerCluster's iconCreateFunction, generates the icon based on the number of public points in the cluster.
ChooseMap.prototype.customCluster = function (cluster) {
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

getPublicChildCount = function (cluster) {
    var pubcount = 0;

    var markers = cluster.getAllChildMarkers()
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
    request.send("data="+encodeURIComponent(data));
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

    cMap = new ChooseMap(points);
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

    cMap.changePoints(points)
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