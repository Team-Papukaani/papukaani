function init(devices, defaultDevice, defaultSpeed) {
    this.sorter = new DeviceSorter(devices, "../rest/gatheringsForIndividual?individualId=");

    map = new PublicMap();

    this.sorter.setMap(map);

    createDummySlider();

    if (defaultDevice != '' && devices.indexOf(defaultDevice) != -1)
        $('#selectDevice').val(defaultDevice);

    if (defaultSpeed != '' && (defaultSpeed % 1) === 0)
        $('#speedSlider').slider("option", "value", defaultSpeed);
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
        this.animation.forwardToEnd();
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
        } else {
            if (this.animation.stop()) {
                $("#play").html("&#9658;");
            }
        }
    }
};

//Performed when the animation reaches its end.
var animationEnd = function () {
    $("#play").html("&#9658;");
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
    var slider = L.DomUtil.get('in-map-slider');
    var play = L.DomUtil.get('in-map-control');
    if (!L.Browser.touch) {
        L.DomEvent.disableClickPropagation(play);
        L.DomEvent.on(play, 'mousewheel', L.DomEvent.stopPropagation);
        L.DomEvent.disableClickPropagation(slider);
        L.DomEvent.on(slider, 'mousewheel', L.DomEvent.stopPropagation);
    } else {
        L.DomEvent.on(play, 'click', L.DomEvent.stopPropagation);
        L.DomEvent.on(slider, 'click', L.DomEvent.stopPropagation);
    }
});

$(function () {
    $("#in-map").on("mouseover", function () {
        $(this).children().css("opacity", 1);
    }).on("mouseout", function () {
        $(this).children().css("opacity", 0.5);
    })
});

//Replaces the slider with a placeholder.
var createDummySlider = function () {
    $("#playSlider").slider = null;
    $("#playLabel").text("N/A");
    $("#playLabel_end").text("");
};

function generateIframeUrl() {
    var inputBox = $('#iframeSrc');
    var url = 'http://' + window.location.hostname + window.location.pathname;
    var device = 'device=' + $('#selectDevice').val();
    var speed = 'speed=' + $('#speedSlider').slider("option", "value");
    inputBox.val(url + '?' + device + '&' + speed);
    inputBox.select()
}

$(function () {
    $(document).ready(function () {
        $('[data-toggle="tooltip"]').tooltip();
    });
});

