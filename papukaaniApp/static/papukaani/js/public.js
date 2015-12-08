function init(devices) {
    this.sorter = new DeviceSorter(devices, "../rest/gatheringsForIndividual?individualId=");
    map = new PublicMap(sorter.documents);

    this.sorter.setMap(map);

    requestPath = function (deviceId) {
    return "../rest/gatheringsForDevice?devId=" + deviceId + "&format=json";
    };

    createDummySlider();
}

function PublicMap() {
    this.map = create_map("map", [61.0, 20.0], 5);
    this.paused = true;
}

//Draws the polyline animation.
PublicMap.prototype.animate = function (latlngs) {
    this.animation = new Animator(latlngs, this.map);
};

//Path for private points REST.
var requestPath = function (deviceId) {
    return "../rest/documentsForDevice?devId=" + deviceId + "&format=json";
};

//Redraws the polyline
PublicMap.prototype.changePoints = function (points) {
    if (this.animation) {
        this.animation.clear();
        this.animation = null;
    }
    try {
        this.latlngs = this.createLatlngsFromPoints(points);
        this.animate(this.latlngs);
    } catch (e) {
    }

//    doc = points[0];
//    pi = new PathIterator(doc.gatherings);
//    time = pi.getStartTime();
};

//Plays the animation if paused, or pauses if currently playing.
PublicMap.prototype.play = function () {
    if (this.animation) {
        if (this.animation.start()) {
            $("#play").html("&#9646;&#9646;");
            $("#playSlider").slider("disable")
        } else {
            if (this.animation.stop()) {
                $("#play").html("&#9658;");
                $("#playSlider").slider("enable");
            }
        }
    }
};

var animationEnd = function () {
    $("#play").attr("disabled", false);
    $("#pause").attr("disabled", true);
    $("#playSlider").slider("enable")
};

//Creates latLng objects from points
PublicMap.prototype.createLatlngsFromPoints = function (points) {
    return points.map(function (point) {
        var coordinates = point.wgs84Geometry.coordinates;
        return {
            coordinates: Victor.fromArray(coordinates.reverse()),
            time: Date.parse(point.dateTimeBegin)
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

//Prevents Leaflet onclick and mousewheel events from triggering when playslider elements used.
$(function () {
    var slider = L.DomUtil.get('playSlider');
    var play = L.DomUtil.get('play');
    var label = L.DomUtil.get('playLabel');
    if (!L.Browser.touch) {
        L.DomEvent.disableClickPropagation(slider);
        L.DomEvent.disableClickPropagation(play);
        L.DomEvent.disableClickPropagation(label);
        L.DomEvent.on(slider, 'mousewheel', L.DomEvent.stopPropagation);
        L.DomEvent.on(play, 'mousewheel', L.DomEvent.stopPropagation);
        L.DomEvent.on(label, 'mousewheel', L.DomEvent.stopPropagation);
    } else {
        L.DomEvent.on(slider, 'click', L.DomEvent.stopPropagation);
        L.DomEvent.on(play, 'click', L.DomEvent.stopPropagation);
        L.DomEvent.on(label, 'click', L.DomEvent.stopPropagation);
    }
});

var createDummySlider = function () {
    $("#playSlider").slider({
        min: 0,
        max: 0,
        step: 0
    });
    $("#playLabel").text("N/A");
};
