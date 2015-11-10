function init(devices) {
    this.sorter = new DeviceSorter(devices);
    map = new PublicMap(sorter.documents);

    sorter.setMap(map)
}

function PublicMap() {
    this.map = create_map("map", [61.0, 20.0], 5);
}


//Draws the polyline animation. i = starting point
PublicMap.prototype.animate = function (latlngs, i) {
    return setTimeout(function () {

            polyline = L.polyline([latlngs[i], latlngs[++i]], {color: 'blue', opacity: 1.0})
            this.polylines.push(polyline);
            polyline.addTo(this.map);
            this.map.panTo(latlngs[i]);
            if (this.polylines.length > 15) {
                this.polylines.splice(0, 1);
            }
            for (j = 0; j < this.polylines.length; j++) {
                this.polylines[j].setStyle({color: 'blue', opacity: (j / 15.0)});
            }

            if(latlngs.length > (i+1)) {
                this.animate(latlngs, i);
            }


        }.bind(this), 1000 - $('#speedSlider').slider("option", "value"))
}


//Redraws the polyline
PublicMap.prototype.changePoints = function (points) {

    var latlngs = this.createLatlngsFromPoints(points);

    this.polylines = [];

    var id = this.animate(latlngs, 0);
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

//SpeedSlider settings
$(function() {
    $( "#speedSlider" ).slider({
        value: 500,
        min: 100,
        max: 1000
    });
});