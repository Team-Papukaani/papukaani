function init(devices) {
    this.sorter = new DeviceSorter(devices);
    map = new PublicMap(sorter.documents);

    this.sorter.setMap(map);
}

function PublicMap() {
    this.map = create_map("map", [61.0, 20.0], 5);
    this.i = 0;
    this.paused = 1;
}

//Draws the polyline animation. i = starting point
PublicMap.prototype.animate = function (latlngs) {
    return setTimeout(function () {
        if (latlngs.length > (this.i + 1)) {
            var polyline = L.polyline([latlngs[this.i], latlngs[++this.i]], {color: 'blue', opacity: 1.0});
            this.polylines.push(polyline);
            polyline.addTo(this.map);
            this.map.panTo(latlngs[this.i]);
            if (this.polylines.length > 4) {
                this.polylines.splice(0, 1);
            }
            for (var j = 0; j < this.polylines.length; j++) {
                this.polylines[j].setStyle({color: 'blue', opacity: polylineFade(j, this.polylines.length)});
            }
            this.animate(latlngs);
        }
    }.bind(this), 1000 - $('#speedSlider').slider("option", "value"));
};

//Picks the opacity-value based on position in the polyline (closer to the head, more opaque).
polylineFade = function (j, length) {
    if (j == length - 1) return 1.0;
    else if (j > 0) return 0.8;
    else return 0.5
};

// Iterates efficiently over objects that have latitude (lat),
// longitude (lng) and time (time) (as milliseconds) as members.
var PathIterator = function (points) {
    var orderedPoints = points.sort(function (a, b) {
        return a.time - b.time
    });
    var currentIndex = 0;

    //Returns the last passed point based on time. If time equals
    //the timestamp of a point, it returns that point.
    this.getPointAtTime = function (time) {
        if (time < this.getStartTime()) return null;
        while (currentIndex < orderedPoints.length - 1 && time >= orderedPoints[currentIndex + 1].time) currentIndex++;
        return orderedPoints[currentIndex];
    };

    //Returns the time (as milliseconds) of the earliest point.
    this.getStartTime = function () {
        return orderedPoints[0].time;
    }
};

//Redraws the polyline
PublicMap.prototype.changePoints = function (points) {

    latlngs = this.createLatlngsFromPoints(points);
    this.i = 0;
    this.paused = 1;
    this.map.clearLayers();
    this.polylines = [];
//    doc = points[0];
//    pi = new PathIterator(doc.gatherings);
//    time = pi.getStartTime();


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

function pause(map) {
    if (!map.paused) {
        clearAllTimeout();
        map.paused = 1;
        $("#selectDevice").attr("disabled", false);
        $("#play").attr("disabled", false);
        $("#pause").attr("disabled", true);
    }
}

function play(map) {
    if (map.paused) {
        map.animate(latlngs);
        map.paused = 0;
        $("#selectDevice").attr("disabled", true);
        $("#play").attr("disabled", true);
        $("#pause").attr("disabled", false);
    }
}


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
        value: 500,
        min: 100,
        max: 1000
    });
});

L.Map.include({
    'clearLayers': function () {
        this.eachLayer(function (layer) {
            if (layer._container.toString().indexOf("SVGG") > -1) {
                this.removeLayer(layer);
            }
        }, this);
    }
});

counter = 2;
function addInput(divName) {
    var newdiv = document.createElement('div');

    newdiv.innerHTML = "<div class='input-group'>\
                <span class='input-group-addon' id='basic-addon1'>Alku:</span>\
                <input type='text' id='start_time" + counter + "' name='start_time" + counter + "' class='dateinput datepicker form-control'\
                       onblur='validateDateFormat(this)'\
                       placeholder='dd-mm-yyyy HH:mm' maxlength='16'>\
            </div>\
            <div class='input-group'>\
                <span class='input-group-addon' id='basic-addon1'>Loppu:</span>\
                <input type='text' id='end_time" + counter + "' name='end_time" + counter + "' class='dateinput datepicker form-control'\
                       onblur='validateDateFormat(this)'\
                       placeholder='dd-mm-yyyy HH:mm' maxlength='16'>\
            </div>";

    counter++;
    document.getElementById(divName).appendChild(newdiv);

    $(".datepicker").datetimepicker();
}

//Updates the map to show all markers within start and end, which are strings that can be converted to Date.
PublicMap.prototype.showMarkersWithinTimeRange = function () {
    var count = 0;
    this.llgroups = [];
    for (var i = 1; i < 10; i++) {
        var latlngs = [];
        try {
            var start = document.getElementById("start_time" + i);
            var end = document.getElementById("end_time" + i);
            counter++;
            messagebox = $("#loading");
            messagebox.text("Tietoja ladataan...");
            lockButtons();
            request = new XMLHttpRequest;
            var path = "../rest/documentsForDevice?devId=" + deviceId + "&start=" + start + "&end=" + end + "&format=json";
            request.open("GET", path, true);
            request.onreadystatechange = addToLLs.bind(this);
            request.send(null);
        } catch (e) {
            messagebox.text("An error has occurred while retrieving information");
            break;
        }
    }
};

addToLLs = function() {
    if (request.readyState === 4) {
        var latlongs = JSON.parse(request.response);
        this.llgroups.push(latlongs);
    }
};