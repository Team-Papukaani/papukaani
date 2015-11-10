function init(devices) {
    this.sorter = new DeviceSorter(devices);
    map = new PublicMap(sorter.documents);

    this.sorter.setMap(map)
}

function PublicMap() {
    this.map = create_map("map", [61.0, 20.0], 5);
}

//Draws the polyline
PublicMap.prototype.draw = function (points) {
    var latlngs = this.createLatlngsFromPoints(points);

    var polylines = [];

    i = 0;
    window.setInterval(function () {
        var polyline = L.polyline([latlngs[i], latlngs[++i]], {color: 'blue', opacity: 1.0});
        polylines.push(polyline);
        polyline.addTo(this.map);
        this.map.panTo(latlngs[i]);
        if (polylines.length > 4) {
            polylines.splice(0, 1);
        }
        for (j = 0; j < polylines.length; j++) {
            polylines[j].setStyle({color: 'blue', opacity: polylineFade(j, polylines.length)});
        }
    }.bind(this), 700);

};

//Picks the opacity-value based on position in the polyline (closer to the head, more opaque).
polylineFade = function(j, length) {
    if (j == length-1) return 1.0;
    else if (j > 0) return 0.8;
    else return 0.5
};

// Iterates efficiently over objects that have latitude (lat),
// longitude (lng) and time (time) (as milliseconds) as members.
var PathIterator = function(points) {
    var orderedPoints = points.sort(function(a, b) {
        return a.time - b.time
    });
    var currentIndex = 0;

    //Returns the last passed point based on time. If time equals
    //the timestamp of a point, it returns that point.
    this.getPointAtTime = function(time) {
        if(time < this.getStartTime()) return null;
        while(currentIndex < orderedPoints.length - 1 && time >= orderedPoints[currentIndex+1].time) currentIndex++;
        return orderedPoints[currentIndex];
    };

    //Returns the time (as milliseconds) of the earliest point.
    this.getStartTime = function() {
        return orderedPoints[0].time;
    }
};

//Redraws the polyline
PublicMap.prototype.changePoints = function (points) {
    this.draw(points);
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