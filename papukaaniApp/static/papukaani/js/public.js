function init(devices) {
    this.sorter = new DeviceSorter(devices);
    map = new PublicMap(sorter.documents);

    this.sorter.setMap(map)
}

function PublicMap() {
    this.map = create_map("map", [61.0, 20.0], 5);
}

//Draws the polyline animation.
PublicMap.prototype.animate = function (latlngs) {
    var pathIterator = new PathIterator(latlngs);

    var polylines = [];
    var markers = [];

    var timeBetweenFirstAndLast = pathIterator.getEndTime() - pathIterator.getStartTime();
    var time = pathIterator.getStartTime();
    var lastPosition = pathIterator.getPositionAtTime(time);
    var markerPosition = lastPosition;
    var marker = L.marker(markerPosition.toArray(), {zIndexOffset: 1000});
    marker.addTo(this.map);

    var loop = setInterval(function () {

        function calculateTimeStep() {
            return $('#speedSlider').slider("option", "value") * timeBetweenFirstAndLast / 24000;
        }

        function updatePolylines(polylines) {
            for (var j = 0; j < Math.min(polylines.length, 40); j++) {
                var line = polylines[j];

                var oldOpacity = line.options.opacity;
                var newOpacity = oldOpacity - 0.02;
                line.setStyle({color: 'blue', opacity: newOpacity});
            }
        }

        function addNewPolyline(polyline) {
            polylines.push(polyline);
            if (polylines.length >= 40) {
                polylines.shift()
            }
            polyline.addTo(this.map);
        }

        var timeStep = calculateTimeStep();
        lastPosition = markerPosition;
        markerPosition = pathIterator.getPositionAtTime(time);

        var polyline = L.polyline([lastPosition.toArray() ,markerPosition.toArray()], {color: 'blue', opacity: 0.9});


        addNewPolyline.call(this, polyline);
        updatePolylines(polylines);

        marker.setLatLng(markerPosition.toArray());
        time += timeStep;
        if (time >= pathIterator.getEndTime()) clearTimeout(loop);
    }.bind(this), 100);
    return loop
};



//Picks the opacity-value based on position in the polyline (closer to the head, more opaque).
polylineFade = function (j) {
    return Math.max(j/200, 0.1);
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
        if(time < this.getStartTime()) return null;
        while(currentIndex < orderedPoints.length - 1 && time >= orderedPoints[currentIndex+1].time) currentIndex++;
        return currentIndex;
    };

    //Returns a linear interpolation of the position
    //of the marker at a given time.
    this.getPositionAtTime = function(time) {
        var pointAIndex = this.getPointIndexAtTime(time);
        var pointA = points[pointAIndex];
        var pointB = points[pointAIndex + 1];

        if(pointB == undefined) {
            pointB = pointA;
        }

        var directionVector = pointB.coordinates.clone().subtract(pointA.coordinates);
        var timeSincePointA = time - pointA.time;
        var pointTimeDifference = pointB.time - pointA.time;
        var directionVectorScalar = timeSincePointA/pointTimeDifference;
        return pointA.coordinates.clone().add(directionVector.multiplyScalar(directionVectorScalar));
    };

    this.getAllPositions = function(timeStep) {
        var traveledPoints = [];
        var currentTime = this.getStartTime();
        var markerPosition = this.getPositionAtTime(currentTime);
        while(currentTime <= this.getEndTime()) {
            traveledPoints.push(this.getPositionAtTime(currentTime).toArray());
            currentTime += timeStep;
        }
        return traveledPoints;
    };

    //Returns the time (as milliseconds) of the earliest point.
    this.getStartTime = function () {
        return orderedPoints[0].time;
    };

    //Returns the time (as milliseconds) of the latest point.
    this.getEndTime = function () {
        return orderedPoints[orderedPoints.length-1].time;
    }
};

//Redraws the polyline
PublicMap.prototype.changePoints = function (points) {

    var latlngs = this.createLatlngsFromPoints(points);
    this.polylines = [];

//    doc = points[0];
//    pi = new PathIterator(doc.gatherings);
//    time = pi.getStartTime();

    var id = this.animate(latlngs);
};


//Creates latLng objects from points
PublicMap.prototype.createLatlngsFromPoints = function (points) {
    return points.map(function(point) {
        var coordinates = point.wgs84Geometry.coordinates;
        return {
            coordinates: Victor.fromArray(coordinates.reverse()),
            time: Date.parse(point.timeStart)
        };
    });
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
        value: 50,
        min: 1,
        max: 100
    });
});