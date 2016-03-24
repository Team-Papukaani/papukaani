//Creates a map where the uploader can select the points which will be published.
var ChooseMap = function(points) {
    this.map = create_map("map", [61.0, 20.0], 5);

    assert(isPoints(points));
    this.points = points;
    this.hasChanges = false;

    this.markers = createEmptyMarkerClusterGroup();

    this.showMarkersWithinTimeRange = this.showMarkersWithinTimeRange.bind(this);

    //True enables cluster spiderfying on all zoom levels. Performance issues with large clusters.
    this.spiderfyOnAnyZoom = false;
}

//Updates the map to show all markers between start and end (strings that can be converted to Date).
ChooseMap.prototype.showMarkersWithinTimeRange = function(start, end) {
    var a, b;
    try {
        a = (start != "" ? new Date(parseTime(start, "+00:00")) : "");
        b = (end != "" ? new Date(parseTime(end, "+00:00")) : "");
    } catch (error) {
        document.getElementById("formatError").innerHTML = gettext("Virheellinen aikaformaatti!");
        return;
    }
    var pointsWithinRange = this.points.filter(function(point) {
        var timestring = point.dateBegin;
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
        if (get_param('nofit') == 1) {} else {
            this.map.fitBounds(this.markers.getBounds(), {
                padding: [6, 6]
            })
        }
    } catch (e) {}
};

var get_param = function(name) {
    if (name = (new RegExp('[?&]' + encodeURIComponent(name) + '=([^&]*)')).exec(location.search))
        return decodeURIComponent(name[1]);
}

//Creates an empty MarkerClusterGroup with initial settings.
var createEmptyMarkerClusterGroup = function() {
    var customCluster = function(cluster) {
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
ChooseMap.prototype.setPoints = function(points) {
    assert(isPoints(points));
    this.hasChanges = false;
    this.points = points;
    var start = $('#start_time').val();
    var end = $('#end_time').val();
    assert($('#start_time').length === 1 && $('#end_time').length === 1);
    this.showMarkersWithinTimeRange(start, end);
};


//Removes all markers from the map.
ChooseMap.prototype.removeAllMarkers = function() {
    this.map.removeLayer(this.markers);
    this.markers = createEmptyMarkerClusterGroup();
};


//Creates markers from point data and adds them to the marker cluster object.
ChooseMap.prototype.createMarkersFromPoints = function(points, markers) {
    for (var i = 0; i < points.length; i++) {
        var ltlgs = points[i].wgs84Geometry.coordinates;
        var marker = L.marker(new L.LatLng(ltlgs[1], ltlgs[0]));
        marker.pnt = points[i];
        marker.on('dblclick', this.changePublicity.bind(this, marker));
        marker.bindPopup(getPopupContentsForMarker(marker), {
            offset: L.point(0, -12)
        });
        marker.on('mouseover', function() {
            this.openPopup();
        });
        marker.on('mouseout', function() {
            this.closePopup();
        });
        marker.off('click');
        markers.addLayer(marker);
    }
    clusterGroup.on('clusterdblclick', this.changeMarkerClusterPublicity.bind(this));
    if (this.spiderfyOnAnyZoom) {
        clusterGroup.on('clusterclick', this.spiderfyAnyZoom.bind(this))
    }
};

//Generates content for marker's popup. Info includes time and all applicable facts.
var getPopupContentsForMarker = function(marker) {
    var content = "";
    content += new Date(marker.pnt.dateBegin).toLocaleString('fi');
    if ("temperature" in marker.pnt) {
        if (marker.pnt.temperature > -273.15) {
            content += "<br>" + gettext("Lämpötila") + ": " + marker.pnt.temperature + "&deg;C";
        }
    }
    return content;
};

//Changes the publicity of every marker in marker cluster a.
ChooseMap.prototype.changeMarkerClusterPublicity = function(a) {
    this.hasChanges = true;

    var markers = a.layer.getAllChildMarkers();
    var changepublicityto = "MZ.publicityRestrictionsPublic";
    if (getPublicChildCount(a.layer) > 0) {
        changepublicityto = "MZ.publicityRestrictionsPrivate";
    }

    for (var i = 0; i < markers.length; i++) {
        changePublicityTo(markers[i], changepublicityto);
        redrawIcon(markers[i]);
    }
    this.markers.refreshClusters(markers);
};

//Spiderfy a cluster.
ChooseMap.prototype.spiderfyAnyZoom = function(a) {
    a.layer.spiderfy();
};

//Forces a redraw of the specified marker's icon, as it doesn't necessarily update when changes are made.
var redrawIcon = function(marker) {
    var c = ' marker-cluster';
    if (marker.pnt.publicityRestrictions === "MZ.publicityRestrictionsPublic") c += '-small';
    else c += '-large';

    marker.setIcon(new L.DivIcon({
        html: '<div><span>' + (marker.pnt.publicityRestrictions === "MZ.publicityRestrictionsPublic" ? 1 : 0) + '/' + 1 + '</span></div>',
        className: 'marker-cluster' + c,
        iconSize: new L.Point(40, 40)
    }));
};

//Reverses the publicity of a marker and updates it.
ChooseMap.prototype.changePublicity = function(marker) {
    this.hasChanges = true;

    marker.pnt.publicityRestrictions = (marker.pnt.publicityRestrictions) === "MZ.publicityRestrictionsPublic" ? "MZ.publicityRestrictionsPrivate" : "MZ.publicityRestrictionsPublic";
    redrawIcon(marker);
    this.markers.refreshClusters(marker);
};

//Changes the publicity of a marker to the desired value.
var changePublicityTo = function(marker, value) {
    marker.pnt.publicityRestrictions = value;
};

//Counts the cluster's public child markers.
var getPublicChildCount = function(cluster) {
    var pubcount = 0;

    var markers = cluster.getAllChildMarkers();
    for (var i = 0; i < markers.length; i++) {
        if (markers[i].pnt.publicityRestrictions == "MZ.publicityRestrictionsPublic") {
            pubcount++;
        }
    }
    return pubcount;
};
