function init(individuals, species, defaultDevice, defaultSpeed, loc, zoom) {
    this.sorter = new DeviceSorter("../rest/gatheringsForIndividual?individualId=");
    this.sorter.setIndividuals(individuals, species);

    zoom = typeof zoom == 'number' ? zoom : 5

    if (!(loc && loc instanceof Array && loc.length == 2 && typeof loc[0] == "number" && typeof loc[1] == "number")) {
        loc = [60, 20]
    }

    map = new PublicMap(loc, zoom);

    createDummySlider();

    this.sorter.setMap(map);

    if (defaultDevice != '') {
        try {
            selector = $('#selectDevice');
            selector.val(defaultDevice);
            this.sorter.changeDeviceSelection(selector.val())
        } catch (err) {
        }
    }

    if (defaultSpeed != '' && (defaultSpeed % 1) === 0)
        $('#speedSlider').slider("option", "value", defaultSpeed);
}

function PublicMap(loc, zoom) {
    this.map = create_map("map", loc, zoom);
    this.paused = true;
}

//Draws the polyline animation.
PublicMap.prototype.animate = function (latlngs, individualname) {
    if (latlngs && individualname) {
        this.animation = new Animator(latlngs, individualname, this.map);
    } else {
        this.animation = null;
    }
};

//Redraws the polyline
PublicMap.prototype.changePoints = function (points) {
    if (this.animation) {
        this.animation.clear();
        this.animation = null;
        createDummySlider();
    }
    if (points) {
        try {
            var individualname = points.pop();
            this.latlngs = this.createLatlngsFromPoints(points);
            this.animate(this.latlngs, individualname);
            this.animation.forwardToEnd();
        } catch (e) {
        }
    }
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
    $("#playSlider").slider({min: 0, max: 0, paddingMin: 7, paddingMax: 7});
    $("#playLabel").text("N/A");
    $("#playLabel_end").text("");
    $("#play").html("&#9658;").prop("disabled", true);
};

function generateIframeUrl() {
    var inputBox = $('#iframeSrc');
    var url = 'http://' + window.location.hostname + window.location.pathname;
    var device = 'device=' + $('#selectDevice').val();
    var speed = 'speed=' + $('#speedSlider').slider("option", "value");
    var zoom = 'zoom=' + map.map.getZoom()
    var ltlng = map.map.getCenter()
    var loc = 'loc=' + "[" + ltlng.lat + "," + ltlng.lng + "]"
    inputBox.val(url + '?' + device + '&' + speed + '&' + zoom + '&' + loc);
    inputBox.select()
}

$(function () {
    $(document).ready(function () {
        $('[data-toggle="tooltip"]').tooltip();
    });
});

