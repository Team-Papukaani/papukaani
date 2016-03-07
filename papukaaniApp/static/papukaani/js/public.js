var request = null;

function IndividualSorter(restUrl, individuals, species, map) {
    this.restUrl = restUrl;
    this.routes = [];
    this.map = map;
    this.birdInfo = {};
    this.createIndividualSelector(individuals, species);
    this.colorChart = new ColorChart();
}
//Sends a request to the rest-controller for documents matching the deviceId.
IndividualSorter.prototype.changeIndividualSelection = function (individualId) {
    $('#loading').modal({
       backdrop: 'static',
       keyboard: false
    })
    request = new XMLHttpRequest;
    var path = this.restUrl + individualId + "&format=json";
    request.open("GET", path, true);
    request.onreadystatechange = showPointsForIndividual.bind(this, individualId);
    request.send(null);
};

IndividualSorter.prototype.removePointsForIndividual = function (individualId) {
    for (var i = 0; i < this.routes.length; i++) {
        if (this.routes[i].individualId == individualId) {
            this.colorChart.freeColor(this.routes[i].individualId);
            player.removeRoute(this.routes[i]);
            this.routes.splice(i, 1);
            $('#selectIndividual').showOption(individualId);
            return;
        }
    }
};

IndividualSorter.prototype.refresh = function () {
    player.refreshRoutes();
};

//Once the request has a response, changes the sorters points to the ones received in the response.
function showPointsForIndividual(ids) {

    if (request.readyState === 4) {
        $('#loading').modal('hide');

        var data = JSON.parse(request.response);

        for (var i = 0; i < ids.length; i++) {

            if (typeof data[ids[i]] === 'undefined') {
                continue;
            }

            var points = data[ids[i]];
            var individualname = points.pop();
            var color = this.colorChart.getColor(ids[i]);

            var route = {
                individualId: ids[i],
                points: points,
                individualname: individualname,
                color: color,
                latlngs: false
            };


            var html = [];
            var id = "individual" + ids[i];
            html.push('<div class="birdrow">');
            html.push('<div data-id="' + ids[i] + '" class="firstCol" id="' + id + '">');
            html.push('<button type="button" class="remove" style="float: left; display: block" aria-hidden="true">' +
                '<span class="glyphicon glyphicon-remove" style="float: left" aria-hidden="true"></span></button>' +
                ' <span>' + individualname + '</span> ');

            if (sorter.getBird(ids[i]).description != "" || sorter.getBird(ids[i]).url != "") {
                html.push('<button type="button" class="showDescription btn btn-info btn-xs" ' +
                          'data-toggle="modal" data-target="#descriptionModal" data-id="' +
                          ids[i] + '">' + gettext('Lisätietoja') + '</button>');
            }
            html.push('</div>');
            html.push('<div class="secondCol" style="background: ' + color + ';">');
            html.push('&nbsp;');
            html.push('</div>');
            html.push('</div>');


            $("#birdies").append(html.join(''));

            this.routes.push(route);
            player.addRoute(route);

        }
        player.refreshRoutes();
        request = null;
    }
}


function ColorChart() {
    this.colors = [{color: "#CC0000"}, {color: "#0000CC"}, {color: "#006600"},
        {color: "#FFFF00"}, {color: "#CC00CC"}, {color: "#666666"}];
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
        color = "#" + ("000000" + color).slice(-6); // ensure color is always six hexadecimals long
    }
    this.colors.push({color: color, individualId: individualId});
    return color;
};

ColorChart.prototype.freeColor = function (individualId) {
    for (var i = 0; i < this.colors.length; i++) {
        if (this.colors[i].individualId == individualId) {
            this.colors[i].individualId = null;
            break;
        }
    }
};

//Creates a selector for individuals (individualId:taxon).
IndividualSorter.prototype.createIndividualSelector = function (individuals, species) {
    var selector = $("#selectIndividual");
    var that = this;

    selector.addOption = function (individualId, taxon) {
        var lang = gettext('fi');
        if (lang != 'fi' && taxon.description != null && (taxon.description[lang] == null || taxon.description[lang] == "")) {
            lang = 'fi';
        }
        var e = '<option value="' + individualId + '">';
        e = e + taxon.nickname;
        e = e + '</option>';
        var bird = {
            name: taxon.nickname,
            url: "",
            description: ""
        };
        if (taxon.descriptionURL !== null && taxon.descriptionURL[lang] !== null &&
            taxon.descriptionURL[lang] !== undefined && taxon.descriptionURL[lang] !== "") {
            bird.url = taxon.descriptionURL[lang];
        }
        if (taxon.description !== null && taxon.description.fi !== null &&
            taxon.description[lang] !== undefined && taxon.description[lang] !== "") {
            bird.description = taxon.description[lang];
        }
        selector.append(e);
        that.birdInfo[individualId] = bird;
    };

    $.each(species, function (key, s) {
        selector.append('<option value="" disabled>' + s + '</option>');
        $.each(individuals[s], function (key, individual) {
            $.each(individual, function (individualId, taxon) {
                selector.addOption(individualId, taxon)
            })
        })
    })

    $("#selectIndividual").change(function () {
        var id = $(this).val();
        if (id === "") return;
        that.changeIndividualSelection([id]);
        $(this).val("");
        $('#selectIndividual').hideOption(id);
    });
};

IndividualSorter.prototype.getBird = function (individualId) {
    return this.birdInfo[individualId];
};

function PublicMap(loc, zoom) {
    this.map = create_map("map", loc, zoom);
    return this.map;
}

function init(individuals, species, individualIds, defaultSpeed, loc, zoom, start_time, end_time) {

    zoom = typeof zoom == 'number' ? zoom : 5;

    if (!(loc && loc instanceof Array && loc.length == 2 && typeof loc[0] == "number" && typeof loc[1] == "number")) {
        loc = [60, 20]
    }

    map = new PublicMap(loc, zoom);

    sorter = new IndividualSorter("../rest/gatheringsForIndividual?individualId=", individuals, species, map);

    player = new Player(map);

    if (start_time !== "") $("#start_time").val(start_time);
    if (end_time !== "") $("#end_time").val(end_time);


    if (individualIds != '') {
        if (individualIds instanceof Array && individualIds.length > 0) {
            var ids = [];
            for (var i = 0; i < individualIds.length; i++) {
                if (typeof individualIds[i] == "number") {
                    try {
                        $("#individual" + individualIds[i]).find('input').prop('checked', true);
                        ids.push(individualIds[i]);
                    } catch (err) {
                    }
                }
            }
            sorter.changeIndividualSelection(ids);
        }
    }

    if (defaultSpeed != '' && (defaultSpeed % 1) === 0)
        $('#speedSlider').slider("option", "value", defaultSpeed);

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
    $("#selectIndividual").attr("disabled", true);
    $("#play").attr("disabled", true);
    $("#pause").attr("disabled", true);
    $("button").attr("disabled", true);
}

//Enables the select, save and reset buttons.
function unlockButtons() {
    $("#selectIndividual").attr("disabled", false);
    $("#play").attr("disabled", false);
    $("#pause").attr("disabled", false);
    $("button").attr("disabled", false);
}
/*
//Prevents Leaflet onclick and mousewheel events from triggering when playslider elements used.
//$(function () {
//    var slider = L.DomUtil.get('in-map-slider');
//    var play = L.DomUtil.get('in-map-control');
//    if (!L.Browser.touch) {
//        L.DomEvent.disableClickPropagation(play);
//        L.DomEvent.on(play, 'mousewheel', L.DomEvent.stopPropagation);
//        L.DomEvent.disableClickPropagation(slider);
//        L.DomEvent.on(slider, 'mousewheel', L.DomEvent.stopPropagation);
//    } else {
//        L.DomEvent.on(play, 'click', L.DomEvent.stopPropagation);
//        L.DomEvent.on(slider, 'click', L.DomEvent.stopPropagation);
//    }
//});
*/
function generateIframeUrl() {
    var inputBox = $('#iframeSrc');
    var url = 'http://' + window.location.hostname + window.location.pathname;

    var ids = [];
    for (var i = 0; i < sorter.routes.length; i++) {
        ids.push(sorter.routes[i].individualId);
    }

    var individuals = 'individuals=[' + ids.join(",") + ']';
    var lang = 'lang=' + $('#language_choose').attr('data-currentlang');

    var speed = 'speed=' + $('#speedSlider').slider("option", "value");

    var zoom = 'zoom=' + player.map.getZoom();
    var ltlng = player.map.getCenter();
    var loc = 'loc=' + "[" + ltlng.lat + "," + ltlng.lng + "]";

    var time = "";

    var start_time = $("#start_time").val();
    var end_time = $("#end_time").val();

    if (start_time !== "" || end_time !== "") {
        time += start_time !== "" ? "&start_time=" + start_time : "";
        time += end_time !== "" ? "&end_time=" + end_time : "";
    }

    inputBox.val(url + '?' + lang + '&' + individuals + '&' + speed + '&' + zoom + '&' + loc + time);
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

