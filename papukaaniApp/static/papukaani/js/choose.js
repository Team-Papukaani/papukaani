//Creates a map where the uploader can select the points which will be published.
function ChooseMap(sorter) {
    this.map = create_map("map", [61.0, 20.0], 5);

    this.sorter = sorter;

    this.markers = createEmptyMarkerClusterGroup();

    this.points = [];

    this.showMarkersWithinTimeRange = this.showMarkersWithinTimeRange.bind(this)

    this.unsaved = false
}

//Updates the map to show all markers within start and end, which are strings that can be converted to Date.
ChooseMap.prototype.showMarkersWithinTimeRange = function (start, end) {
    var a, b;
    try {
        a = (start != "" ? new Date(parseTime(start, "+00:00")) : "");
        b = (end != "" ? new Date(parseTime(end, "+00:00")) : "");
    } catch (error) {
        document.getElementById("formatError").innerHTML = "Invalid Date format!";
        return;
    }
    var pointsWithinRange = this.points.filter(function (point) {
        var timestring = point.dateTimeBegin;
        var timestamp = new Date(timestring);
        a = (start != "" ? a : timestamp);
        b = (end != "" ? b : timestamp);
        return dateIsBetween(timestamp, a, b)
    });
    this.removeAllMarkers.call(this);
    this.createMarkersFromPoints(pointsWithinRange, this.markers);
    this.map.points = pointsWithinRange;
    this.map.addLayer(this.markers);
    try {
        if (get('nofit') == 1) {
        } else {
            this.map.fitBounds(this.markers.getBounds(), {padding: [6, 6]})
        }
    } catch (e) {
    }
};

function get(name) {
    if (name = (new RegExp('[?&]' + encodeURIComponent(name) + '=([^&]*)')).exec(location.search))
        return decodeURIComponent(name[1]);
}

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
        maxClusterRadius: 35,
        singleMarkerMode: true,
        spiderfyOnMaxZoom: true,
        iconCreateFunction: customCluster
    });
    return clusterGroup
}

//Changes the currently visible points to the ones given, taking into account the current time-selection.
ChooseMap.prototype.changePoints = function (points) {
    this.unsaved = false;
    this.points = points;
    var start = document.getElementById("start_time");
    var end = document.getElementById("end_time");
    this.showMarkersWithinTimeRange(start.value, end.value);
};

//Removes all markers from the map.
ChooseMap.prototype.removeAllMarkers = function () {
    this.map.removeLayer(this.markers);
    this.markers = createEmptyMarkerClusterGroup();
};


//Creates markers from point data and adds them to the marker cluster object.
ChooseMap.prototype.createMarkersFromPoints = function (points, markers) {
    for (var i = 0; i < points.length; i++) {
        var ltlgs = points[i].wgs84Geometry.coordinates;
        var marker = L.marker(new L.LatLng(ltlgs[1], ltlgs[0]));
        marker.pnt = points[i];
        marker.on('dblclick', this.changePublicity.bind(this, marker));
        marker.bindPopup(getPopupContentsForMarker(marker), {offset: L.point(0, -12)});
        marker.on('mouseover', function () {
            this.openPopup();
        });
        marker.on('mouseout', function () {
            this.closePopup();
        });
        marker.off('click');
        markers.addLayer(marker);
    }
    clusterGroup.on('clusterdblclick', this.changeMarkerClusterPublicity.bind(this));
};

var getPopupContentsForMarker = function (marker) {
    var content = "";
    content += new Date(marker.pnt.dateTimeBegin).toLocaleString();
    if ("temperatureCelsius" in marker.pnt) {
        if (marker.pnt.temperatureCelsius > -273.15) {
            content += "<br>" + "Temperature: " + marker.pnt.temperatureCelsius + "&deg;C";
        }
    }
    var facts = marker.pnt.facts;
    for (var a in facts) {
        if (a.name == "altitude") {
            content += "<br>" + "Altitude: " + a.value;
        }
    }
    return content;
};

//Changes the publicity of every marker in marker cluster a.
ChooseMap.prototype.changeMarkerClusterPublicity = function (a) {
    this.unsaved = true;

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

//Posts publicity data to server. Shows a message and disables the save button while waiting for response.
ChooseMap.prototype.send = function () {
    data = JSON.stringify({deviceId :  this.sorter.currentDevice ,gatherings : this.sorter.points});
    var messagebox = $("#loading");
    messagebox.text("Tallennetaan...");

    lockButtons();

    request = new XMLHttpRequest;

    request.onreadystatechange = function () {
        setLoadingMessage(request, messagebox)
    };

    request.open("POST", "", true);
    set_headers(csrf_token, request);
    request.send("data=" + encodeURIComponent(data));

    this.unsaved = false
};


//Forces a redraw of the specified marker's icon, as it doesn't necessarily update when changes are made.
redrawIcon = function (marker) {
    var c = ' marker-cluster';
    if (marker.pnt.publicity === "public") c += '-small';
    else c += '-large';

    marker.setIcon(new L.DivIcon({
        html: '<div><span>' + (marker.pnt.publicity === "public" ? 1 : 0) + '/' + 1 + '</span></div>',
        className: 'marker-cluster' + c,
        iconSize: new L.Point(40, 40)
    }));
};

//Reverses the publicity of a marker and updates it.
ChooseMap.prototype.changePublicity = function (marker) {
    this.unsaved = true;

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


//Sets the content type and CSRF token cookie headers.
function set_headers(csrf_token, request) {
    request.setRequestHeader("X-CSRFToken", csrf_token);
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
}

//Callback function for post request. Shows a message depending on response status.
function setLoadingMessage(request, messagebox) {
    if (request.readyState == 4) {
        unlockButtons();
        if (request.status == 200) {
            messagebox.text("Valmis!");
        } else {
            messagebox.text("Tapahtui virhe!");
        }
    }
}

function init(devices, token) {
    this.sorter = new DeviceSorter(devices, "../rest/gatheringsForDevice?devId=");

    map = new ChooseMap(sorter);
    this.sorter.setMap(map);
    csrf_token = token;

    return map
}

//Resets the map to the state it was in when the page was loaded.
function resetMap(map) {
    map.unsaved = false;
    map.map.removeLayer(map.markers);
    map.markers = createEmptyMarkerClusterGroup();
    map.map.addLayer(map.markers);
    map.sorter.resetOption();
    map.sorter.documents = [];
    map.points = [];
    document.getElementById("start_time").value = "";
    document.getElementById("end_time").value = "";
}

//Disables the select, save and reset buttons.
function lockButtons() {
    $("#selectDevice").attr("disabled", true);
    $("#save").attr("disabled", true);
    $("#reset").attr("disabled", true);
}

//Enables the select, save and reset buttons.
function unlockButtons() {
    $("#selectDevice").attr("disabled", false);
    $("#save").attr("disabled", false);
    $("#reset").attr("disabled", false);
}