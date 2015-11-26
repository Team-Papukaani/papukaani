function Animator(latlngs, map) {
    this.map = map;
    this.pathIterator = new PathIterator(latlngs);

    this.polylines = [];

    this.timeBetweenFirstAndLast = this.pathIterator.getEndTime() - this.pathIterator.getStartTime();
    this.time = this.pathIterator.getStartTime();
    this.lastPosition = this.pathIterator.getPositionAtTime(this.time);
    this.markerPosition = this.lastPosition;
    this.marker = L.marker(this.markerPosition.toArray(), {zIndexOffset: 1000});
    this.marker.addTo(this.map);
    this.marker.bindPopup(this.getMarkerTimeStamp());

    this.paused = true;
}

Animator.prototype.getMarkerTimeStamp = function () {
    var date = new Date(this.time);
    return new Intl.DateTimeFormat('fi-FI', {weekday: 'short', day: 'numeric', month: 'long', year: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric', timeZoneName: 'short'}).format(date);
};

//Animates the polylines and the marker on the map.
Animator.prototype.animate = function () {
    this.interval = setInterval(function () {

        function calculateTimeStep(time) {
            return $('#speedSlider').slider("option", "value") * time / 24000;
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
            this.polylines.push(polyline);
            if (this.polylines.length >= 40) {
                this.polylines.shift()
            }
            polyline.addTo(this.map);
        }

        var timeStep = calculateTimeStep(this.timeBetweenFirstAndLast);
        this.lastPosition = this.markerPosition;
        this.markerPosition = this.pathIterator.getPositionAtTime(this.time);

        var polyline = L.polyline([this.lastPosition.toArray(), this.markerPosition.toArray()], {
            color: 'blue',
            opacity: 0.9
        });

        addNewPolyline.call(this, polyline);
        updatePolylines(this.polylines);

        this.marker.setLatLng(this.markerPosition.toArray());
        this.marker._popup.setContent(this.getMarkerTimeStamp());
        this.time += timeStep;
        if (this.time >= this.pathIterator.getEndTime()) clearTimeout(this.interval);
    }.bind(this), 100);
};

//Starts the animation.
Animator.prototype.start = function () {
    if (this.paused) {
        this.animate();
        this.paused = false;
        return true;
    }
};

//Stops the animation.
Animator.prototype.stop = function () {
    if (!this.paused) {
        clearInterval(this.interval);
        this.paused = true;
        return true;
    }
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
    this.getPointAtTime = function (time) {
        var pointIndex = this.getPointIndexAtTime(time);
        if (pointIndex == undefined) return null;
        return orderedPoints[pointIndex];
    };

    //Helper function
    this.getPointIndexAtTime = function (time) {
        if (time < this.getStartTime()) return null;
        while (currentIndex < orderedPoints.length - 1 && time >= orderedPoints[currentIndex + 1].time) currentIndex++;
        return currentIndex;
    };

    //Returns a linear interpolation of the position
    //of the marker at a given time.
    this.getPositionAtTime = function (time) {
        var pointAIndex = this.getPointIndexAtTime(time);
        var pointA = points[pointAIndex];
        var pointB = points[pointAIndex + 1];

        if (pointB == undefined) {
            pointB = pointA;
        }

        var directionVector = pointB.coordinates.clone().subtract(pointA.coordinates);
        var timeSincePointA = time - pointA.time;
        var pointTimeDifference = pointB.time - pointA.time;
        var directionVectorScalar = timeSincePointA / pointTimeDifference;
        return pointA.coordinates.clone().add(directionVector.multiplyScalar(directionVectorScalar));
    };

    this.getAllPositions = function (timeStep) {
        var traveledPoints = [];
        var currentTime = this.getStartTime();
        var markerPosition = this.getPositionAtTime(currentTime);
        while (currentTime <= this.getEndTime()) {
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
        return orderedPoints[orderedPoints.length - 1].time;
    };
};

//Removes the animation, effectively removing all markers and polylines created by it.
Animator.prototype.clear = function () {
    this.stop();
    this.map.removeLayer(this.marker);
    this.map.clearLayers();
    delete this;
};

L.Map.include({
    'clearLayers': function () {
        this.eachLayer(function (layer) {
            if (layer._container.toString().indexOf("SVGG") > -1) {
                this.removeLayer(layer);
            }
        }, this);
    }
});
