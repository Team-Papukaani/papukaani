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
        this.setSliderValues();
    } catch (e) {
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

PublicMap.prototype.setSliderValues = function () {

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

//Prevents Leaflet onclick and mousewheel events from triggering when slider is used.
$(function () {
    var div = L.DomUtil.get('playSlider');
    if (!L.Browser.touch) {
        L.DomEvent.disableClickPropagation(div);
        L.DomEvent.on(div, 'mousewheel', L.DomEvent.stopPropagation);
    } else {
        L.DomEvent.on(div, 'click', L.DomEvent.stopPropagation);
    }
});

//Initializes a slider with an attached label showing current value.
$(function () {
    $("#playSlider").slider({
        min: 0,
        max: 0,
        step: 0,
        values: [0],
        slide: function (event, ui) {
            var delay = function () {
                var label = '#playLabel';
                $(label).html(ui.value).position({
                    my: 'center top',
                    at: 'center bottom',
                    of: ui.handle
                }).css({visibility: 'visible'});
            };

            // wait for the ui.handle to set its position
            setTimeout(delay, 5);
        }
    });
});
