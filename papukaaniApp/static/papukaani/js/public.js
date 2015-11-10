function init(devices) {
    this.sorter = new DeviceSorter(devices);
    map = new PublicMap(sorter.documents);

    sorter.setMap(map)
}

function PublicMap() {
    this.map = create_map("map", [61.0, 20.0], 5);
}

//Draws the polyline
PublicMap.prototype.draw = function (points) {
    var latlngs = this.createLatlngsFromPoints(points);

    polylines = [];
    i = 0;
    window.setInterval(function () {
        polyline = L.polyline([latlngs[i], latlngs[++i]], {color: 'blue', opacity: 1.0});
        polylines.push(polyline);
        polyline.addTo(this.map);
        this.map.panTo(latlngs[i]);
        if (polylines.length > 4) {
            polylines.splice(0, 1);
        }
        for (j = 1; j <= polylines.length; j++) {
            polylines[j-1].setStyle({color: 'blue', opacity: ((j/polylines.length) >= 0.5 ? j/polylines.length:0.4)});
        }
    }.bind(this), 700);

};

//Redraws the polyline
PublicMap.prototype.changePoints = function (points) {
    this.draw(points);
};


//Creates latLng objects from points
PublicMap.prototype.createLatlngsFromPoints = function (points) {
    var latlngs = [];
    for (var p = 0; p < points.length; p++) {
        var ltlgs = points[p].wgs84Geometry.coordinates;
        latlngs.push([ltlgs[1], ltlgs[0]]);
    }
    return latlngs;
};

//Disables the select, save and reset buttons.
function lockButtons() {
    $("#selectDevice").attr("disabled", true);
}

//Enables the select, save and reset buttons.
function unlockButtons() {
    $("#selectDevice").attr("disabled", false);
}