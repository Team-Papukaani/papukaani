function init(devices) {
    this.sorter = new DeviceSorter(devices);
    map = new PublicMap(sorter.documents);

    sorter.setMap(map)
}

function PublicMap() {
    this.map = create_map("map", [61.0, 20.0], 5);
}

//Draws the polyline
PublicMap.prototype.draw = function (points) {
    doc = points[0];
    pi = new PathIterator(doc.gatherings);
    polylines = [];
    time = pi.getStartTime();

    i = 0;
    window.setInterval(function () {
        polyline = L.polyline([latlngs[i], latlngs[++i]], {color: 'blue', opacity: 1.0})
        polylines.push(polyline);
        polyline.addTo(this.map);
        this.map.panTo(latlngs[i]);
        if (polylines.length > 15) {
            polylines.splice(0, 1);
        }
        for (j = 0; j < polylines.length; j++) {
            polylines[j].setStyle({color: 'blue', opacity: (j / 15.0)});
        }
    }.bind(this), 700);

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
        var pointIndex = this.getPointIndexAtTime(time);
        if(pointIndex == undefined) return null;
        return orderedPoints[pointIndex];
    }

    this.getPointIndexAtTime = function(time) {
        if(time < this.getStartTime()) return null
        while(currentIndex < orderedPoints.length - 1 && time >= orderedPoints[currentIndex+1].time) currentIndex++;
        return currentIndex;
    }

    this.getPositionAtTime = function(time) {
        var pointAIndex = this.getPointIndexAtTime(time);
        var pointA = points[pointAIndex]
        var pointB = points[pointAIndex + 1]

        var pointAVector = new Victor(pointA.lat, pointA.lng);
        var pointBVector = new Victor(pointB.lat, pointB.lng);

        var directionVector = pointBVector.clone().subtract(pointAVector);
        var timeSincePointA = time - pointA.time;
        var pointTimeDifference = pointB.time - pointA.time;
        var directionVectorScalar = timeSincePointA/pointTimeDifference;
        return pointAVector.add(directionVector.multiplyScalar(directionVectorScalar));
    }

    //Returns the time (as milliseconds) of the earliest point.
    this.getStartTime = function() {
        return orderedPoints[0].time;
    }
}

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