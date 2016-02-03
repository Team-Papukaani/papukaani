function IndividualSorter(restUrl, individuals, species, map) {
    this.restUrl = restUrl;
    this.routes = [];
    this.map = map;
    this.createIndividualSelector(individuals, species);
}

//Sends a request to the rest-controller for documents matching the deviceId.
IndividualSorter.prototype.changeDeviceSelection = function (individualId) {
    var messagebox = $("#loading");
    messagebox.text("Tietoja ladataan...");
    lockButtons();
    request = new XMLHttpRequest;
    var path = this.restUrl + individualId + "&format=json";
    request.open("GET", path, true);
    request.onreadystatechange = showPointsForIndividual.bind(this, individualId);
    request.send(null);
};

IndividualSorter.prototype.removePointsForIndividual = function (individualId) {
    for (var i = 0; i < this.routes.length; i++) {
        if (this.routes[i].individualId === individualId) {
            if (this.routes[i].animation) {
                this.routes[i].animation.clear();
                this.routes[i].animation = null;
            }
            this.routes.splice(i, 1);
            this.map.changePoints(this.routes);
            return;
        }
    }
}

//Once the request has a response, changes the sorters points to the ones received in the response.
function showPointsForIndividual(individualId) {
    if (request.readyState === 4) {

        var messagebox = $("#loading");
        messagebox.text("");

        var points = JSON.parse(request.response);

        if (points.length == 0) {
            $("#selectIndividual input").attr("disabled", false);
        } else {
            var individualname = points.pop();
            this.routes.push({
                individualId: individualId,
                points: points,
                individualname: individualname,
                color: '#'+(Math.random()*0xFFFFFF<<0).toString(16),
                latlngs: false
            });

            this.map.changePoints(this.routes);
            unlockButtons();
        }
    }
}

//Creates a selector for individuals (individualId:taxon).
IndividualSorter.prototype.createIndividualSelector = function (individuals, species) {
    var selector = $("#selectIndividual");
    var that = this;

    selector.addOption = function (individualId, taxon) {
        selector.append('<li><label><input type="checkbox" value="' + individualId + '">' + taxon + '</label></li>')
    };

    $.each(species, function (key, s) {
        selector.append("<li>" + s + "</li>")
        $.each(individuals[s], function (key, individual) {
            $.each(individual, function (individualId, taxon) {
                selector.addOption(individualId, taxon)
            })
        })
    })

    $("#selectIndividual input").change(function () {
        if ($(this).is(":checked")) {
            that.changeDeviceSelection($(this).val())
        } else {
            that.removePointsForIndividual($(this).val())
        }
    });
};

function init(individuals, species, defaultDevice, defaultSpeed, loc, zoom, start_time, end_time) {

    zoom = typeof zoom == 'number' ? zoom : 5;

    if (!(loc && loc instanceof Array && loc.length == 2 && typeof loc[0] == "number" && typeof loc[1] == "number")) {
        loc = [60, 20]
    }

    map = new PublicMap(loc, zoom);

    sorter = new IndividualSorter("../rest/gatheringsForIndividual?individualId=", individuals, species, map);

    playSliderKeyboardControls();

    createDummySlider();

    if (start_time !== "") $("#start_time").val(start_time);
    if (end_time !== "") $("#end_time").val(end_time);


    if (defaultDevice != '') {
        try {
            selector = $('#selectIndividual');
            selector.val(defaultDevice);
            sorter.changeDeviceSelection(selector.val())
        } catch (err) {
        }
    }

    if (defaultSpeed != '' && (defaultSpeed % 1) === 0)
        $('#speedSlider').slider("option", "value", defaultSpeed);
}

//Add play-on-spacebar-press to the map div, and prevent propagation of said event when play button is selected.
var playSliderKeyboardControls = function () {
    $('#map').bind('keyup', function (event) {
        if (event.keyCode == 32) {
            map.play();
        }
    });

    $('#play').keyup(function (e) {
        if (e.keyCode == 32) {
            e.stopPropagation();
        }
    });

    //Prevent screen scrolling when spacebar pressed.
    window.onkeydown = function (e) {
        var elem = e.target.nodeName;
        if (e.keyCode == 32 && elem != "INPUT") {
            e.preventDefault();
            return false;
        }
    };
};

function PublicMap(loc, zoom) {
    this.map = create_map("map", loc, zoom);
}

//Redraws the polyline
PublicMap.prototype.changePoints = function (routes) {
    for (var i = 0; i < routes.length; i++) {

        var start = $("#start_time").val();
        var end = $("#end_time").val();
        var points = points_in_timerange(routes[i].points, start, end);

        if (routes[i].animation) {
            routes[i].animation.clear();
            routes[i].animation = null;
        }

        if (points.length > 0) {
            try {
                if (routes[i].latlngs === false) {
                    routes[i].latlngs = this.createLatlngsFromPoints(points);
                }
                routes[i].animation = new Animator(routes[i].latlngs, routes[i].individualname, this.map, routes[i].color);
                routes[i].animation.forwardToEnd();

            } catch (e) {
            }
        }
    }
    this.routes = routes;
};

//Plays the animation if paused, or pauses if currently playing.
PublicMap.prototype.play = function () {
    for (var i = 0; i < this.routes.length; i++) {
        if (this.routes[i].animation) {
            if (this.routes[i].animation.start()) {
                animationStart();
            } else if (this.routes[i].animation.stop()) {
                animationEnd();
            }
        }
    }
};
var animationStart = function () {
    $("#play").html("&#9646;&#9646;");
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
    $("#selectIndividual input").attr("disabled", true);
    $("#play").attr("disabled", true);
    $("#pause").attr("disabled", true);
}

//Enables the select, save and reset buttons.
function unlockButtons() {
    $("#selectIndividual input").attr("disabled", false);
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

    var device = 'device=' + $('#selectIndividual').val();
    var speed = 'speed=' + $('#speedSlider').slider("option", "value");

    var zoom = 'zoom=' + map.map.getZoom();
    var ltlng = map.map.getCenter();
    var loc = 'loc=' + "[" + ltlng.lat + "," + ltlng.lng + "]";

    var time = "";

    var start_time = $("#start_time").val();
    var end_time = $("#end_time").val();

    if (start_time !== "" || end_time !== "") {
        time += start_time !== "" ? "&start_time=" + start_time : "";
        time += end_time !== "" ? "&end_time=" + end_time : "";
    }

    inputBox.val(url + '?' + device + '&' + speed + '&' + zoom + '&' + loc + time);
    inputBox.select()
}

$(function () {
    $(document).ready(function () {
        $('[data-toggle="tooltip"]').tooltip();
    });
});

function points_in_timerange(points, start, end) {
    var a = start !== "" ? new Date(parseTime(start, "+00:00")) : new Date(1900, 1, 1, 0, 0, 0, 0);
    var b = end !== "" ? new Date(parseTime(end, "+00:00")) : new Date();

    var pts = [];

    for (var i = 0; i < points.length; i++) {
        if (dateIsBetween(new Date(points[i].dateTimeBegin), a, b)) {
            pts.push(points[i])
        }
    }

    return pts
}
