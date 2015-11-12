function init(devices) {
    this.sorter = new DeviceSorter(devices);
    map = new PublicMap(sorter.documents);

    this.sorter.setMap(map)
}

function PublicMap() {
    this.map = create_map("map", [61.0, 20.0], 5);
}

//Draws the polyline animation. i = starting point
PublicMap.prototype.animate = function (latlngs, i) {
    return setTimeout(function () {

        var polyline = L.polyline([latlngs[i], latlngs[++i]], {color: 'blue', opacity: 1.0})
        this.polylines.push(polyline);
        polyline.addTo(this.map);
        this.map.panTo(latlngs[i]);
        if (this.polylines.length > 4) {
            this.polylines.splice(0, 1);
        }
        for (var j = 0; j < this.polylines.length; j++) {
            this.polylines[j].setStyle({color: 'blue', opacity: polylineFade(j, this.polylines.length)});
        }

        if (latlngs.length > (i + 1)) {
            this.animate(latlngs, i);
        }


    }.bind(this), 1000 - $('#speedSlider').slider("option", "value"))
};

//Picks the opacity-value based on position in the polyline (closer to the head, more opaque).
polylineFade = function (j, length) {
    if (j == length - 1) return 1.0;
    else if (j > 0) return 0.8;
    else return 0.5
};

// Iterates efficiently over objects that have coordinates as a Victor
// and time (time) (as milliseconds) as members.
var PathIterator = function (points) {
    var orderedPoints = points.sort(function (a, b) {
        return a.time - b.time
    });
    var currentIndex = 0;

    //Returns the last passed point based on time. If time equals
    //the timestamp of a point, it returns that point.
    this.getPointAtTime = function(time) {
        var pointIndex = this.getPointIndexAtTime(time);
        if(pointIndex == undefined) return null;
        return orderedPoints[pointIndex];
    };

    //Helper function
    this.getPointIndexAtTime = function(time) {
        if(time < this.getStartTime()) return null
        while(currentIndex < orderedPoints.length - 1 && time >= orderedPoints[currentIndex+1].time) currentIndex++;
        return currentIndex;
    };

    //Returns a linear interpolation of the position
    //of the marker at a given time.
    this.getPositionAtTime = function(time) {
        var pointAIndex = this.getPointIndexAtTime(time);
        var pointA = points[pointAIndex]
        var pointB = points[pointAIndex + 1]

        var directionVector = pointB.coordinates.clone().subtract(pointA.coordinates);
        var timeSincePointA = time - pointA.time;
        var pointTimeDifference = pointB.time - pointA.time;
        var directionVectorScalar = timeSincePointA/pointTimeDifference;
        return pointA.coordinates.clone().add(directionVector.multiplyScalar(directionVectorScalar));
    };

    //Returns the time (as milliseconds) of the earliest point.
    this.getStartTime = function () {
        return orderedPoints[0].time;
    }
};

//Redraws the polyline
PublicMap.prototype.changePoints = function (points) {

    var latlngs = this.createLatlngsFromPoints(points);
    this.polylines = [];

//    doc = points[0];
//    pi = new PathIterator(doc.gatherings);
//    time = pi.getStartTime();

    var id = this.animate(latlngs, 0);
};


//Creates latLng objects from points
PublicMap.prototype.createLatlngsFromPoints = function (points) {
    return points.map(function(point) {
        var coordinates = point.wgs84Geometry.coordinates;
        return {
            coordinates: Victor.fromArray(coordinates),
            time: Date.parse(point.timeStart)
        };
    });

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

//SpeedSlider settings
$(function () {
    $("#speedSlider").slider({
        value: 500,
        min: 100,
        max: 1000
    });
});
