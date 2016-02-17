var request = null;

function IndividualSorter(restUrl, individuals, species, map) {
    this.restUrl = restUrl;
    this.routes = [];
    this.map = map;
    this.createIndividualSelector(individuals, species);
    this.colorChart = new ColorChart();
}
/*

IndividualSorter.prototype.getRoutes = function () {
    return this.routes;
}

*/
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
            /*
            if (this.routes[i].animation) {
                this.routes[i].animation.clear();
                this.routes[i].animation = null;
            }
            */

            this.colorChart.freeColor(this.routes[i].individualId);
            player.removeRoute(this.routes[i]);
            this.routes.splice(i, 1);
            //this.map.changePoints(this.routes);
            $("#individual" + individualId).find("div.sqr").css('background-color', "#fff");
            return;
        }
    }
}
/*
IndividualSorter.prototype.refresh = function () {
    this.map.changePoints(this.routes);
}
*/

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

            var indiv = $("#individual" + individualId);
            var color = this.colorChart.getColor(individualId);
            indiv.find("div.sqr").css('background-color', color);

            var route = {
                individualId: individualId,
                points: points,
                individualname: individualname,
                color: color,
                latlngs: false
            };

            this.routes.push(route);
            player.addRoute(route);
            player.showRoute(route);

            //this.map.changePoints(this.routes);
            unlockButtons();
        }
        request = null;
    }
}


function ColorChart() {
    this.colors = [{color: "#CC0000"}, {color: "#FFFF00"}, {color: "#00CC00"},
        {color: "#00FFFF"}, {color: "#0000CC"}, {color: "#CC00CC"},
        {color: "#808080"}];
}


ColorChart.prototype.getColor = function (individualId) {
    var color;
    for (var i = 0; i < this.colors.length; i++) {
        if (!this.colors[i].individualId) {
            color = this.colors[i].color;
            this.colors[i].individualId = individualId;
            break;
        }
    }
    if (!color) {
        color = (Math.random() * 0xFFFFFF << 0).toString(16);
        color = "#" + ("FFFFFF" + color).slice(-6); // ensure color is always six hexadecimals long
    }
    this.colors.push({color: color, individualId: individualId});
    return color;
}

ColorChart.prototype.freeColor = function (individualId) {
    for (var i = 0; i < this.colors.length; i++) {
        if (this.colors[i].individualId == individualId) {
            this.colors[i].individualId = null;
            break;
        }
    }
}

//Creates a selector for individuals (individualId:taxon).
IndividualSorter.prototype.createIndividualSelector = function (individuals, species) {
    var selector = $("#selectIndividual");
    var that = this;

    selector.addOption = function (individualId, taxon) {

        var color = (Math.random() * 0xFFFFFF << 0).toString(16);
        color = "#" + ("FFFFFF" + color).slice(-6); // ensure color is always six hexadecimals long

        var e = '<li id="individual' + individualId + '">';
        e = e + '<label><input type="checkbox" style="display:none;" value="' + individualId + '">';
        e = e + '<div class="sqr"></div>';
        e = e + '<span>' + taxon + '</span>';
        e = e + '</label>';
        e = e + '</li>';
        selector.append(e);
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

function PublicMap(loc, zoom) {
    this.map = create_map("map", loc, zoom);
    return this.map;
}

function init(individuals, species, defaultDevice, defaultSpeed, loc, zoom, start_time, end_time) {

    zoom = typeof zoom == 'number' ? zoom : 5;

    if (!(loc && loc instanceof Array && loc.length == 2 && typeof loc[0] == "number" && typeof loc[1] == "number")) {
        loc = [60, 20]
    }

    map = new PublicMap(loc, zoom);

    sorter = new IndividualSorter("../rest/gatheringsForIndividual?individualId=", individuals, species, map);

    player = new Player(map);

/*

    playSliderKeyboardControls();

    createDummySlider();

    if (start_time !== "") $("#start_time").val(start_time);
    if (end_time !== "") $("#end_time").val(end_time);


    if (defaultDevice != '') {
        if (defaultDevice instanceof Array && defaultDevice.length > 0) {
            for (var i = 0; i < defaultDevice.length; i++) {
                if (typeof defaultDevice[i] == "number") {
                    try {
                        $("#individual" + defaultDevice[i]).find('input').prop('checked', true);
                        sorter.changeDeviceSelection(defaultDevice[i]);
                    } catch (err) {
                    }
                }
            }
        }
    }

    if (defaultSpeed != '' && (defaultSpeed % 1) === 0)
        $('#speedSlider').slider("option", "value", defaultSpeed);
        */
}
/*
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

*/

/*

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
            time: Date.parse(point.dateBegin)
        };
    });
};

*/
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
/*
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

    var checked = $('#selectIndividual input:checked');
    var a = [];
    for (var i = 0; i < checked.length; i++) {
        a.push(checked[i].value);
    }

    var device = 'device=[' + a.join(",") + ']';

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
        if (dateIsBetween(new Date(points[i].dateBegin), a, b)) {
            pts.push(points[i])
        }
    }

    return pts
}
*/