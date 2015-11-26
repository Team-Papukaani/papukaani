function init(devices) {
    this.sorter = new DeviceSorter(devices);
    map = new PublicMap(sorter.documents);

    this.sorter.setMap(map)
}

function PublicMap() {
    this.map = create_map("map", [61.0, 20.0], 5);
    this.paused = true;
}

//Draws the polyline animation.
PublicMap.prototype.animate = function (latlngs) {
    this.animation = new Animator(latlngs, this.map);
};

//Redraws the polyline
PublicMap.prototype.changePoints = function (points) {
    if (this.animation) {
        this.animation.clear();
    }
    try {
        this.latlngs = this.createLatlngsFromPoints(points);
        this.animate(this.latlngs);
    }   catch (e) {
    }

//    doc = points[0];
//    pi = new PathIterator(doc.gatherings);
//    time = pi.getStartTime();

};

PublicMap.prototype.play = function () {
    if (this.animation.start()) {
        $("#play").attr("disabled", true);
        $("#pause").attr("disabled", false);
    }
};

PublicMap.prototype.pause = function () {
    if (this.animation.stop()) {
        $("#play").attr("disabled", false);
        $("#pause").attr("disabled", true);
    }
};


//Creates latLng objects from points
PublicMap.prototype.createLatlngsFromPoints = function (points) {
    return points.map(function (point) {
        var coordinates = point.wgs84Geometry.coordinates;
        return {
            coordinates: Victor.fromArray(coordinates.reverse()),
            time: Date.parse(point.timeStart)
        };
    });
};

//Disables the select, save and reset buttons.
function lockButtons() {
    $("#selectDevice").attr("disabled", true);
    $("#play").attr("disabled", true);
    $("#pause").attr("disabled", true);
}

//Enables the select, save and reset buttons.
function unlockButtons() {
    $("#selectDevice").attr("disabled", false);
    $("#play").attr("disabled", false);
    $("#pause").attr("disabled", false);
}

//SpeedSlider settings
$(function () {
    $("#speedSlider").slider({
        value: 50,
        min: 1,
        max: 100
    });
});

