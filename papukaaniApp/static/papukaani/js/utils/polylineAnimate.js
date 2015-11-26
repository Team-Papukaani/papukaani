function Animator(latlngs, map) {
    this.map = map;
    this.latlngs = latlngs;
    this.pathIterator = new PathIterator(latlngs);

    this.polylines = [];

    this.timeBetweenFirstAndLast = this.pathIterator.getEndTime() - this.pathIterator.getStartTime();
    this.time = this.pathIterator.getStartTime();
    this.lastPosition = this.pathIterator.getPositionAtTime(this.time);
    this.markerPosition = this.lastPosition;
    this.marker = L.marker(this.markerPosition.toArray(), {zIndexOffset: 1000});
    this.polyline = L.polyline([], {
        color: 'blue',
        opacity: 0.2
    });
    this.polyline.addTo(this.map);
    this.marker.addTo(this.map);
    this.marker.bindPopup(this.getMarkerTimeStamp());

    this.paused = true;
    createSlider(this.pathIterator.getStartTime(), this.pathIterator.getEndTime(), 1000);
    setSliderValue(this.pathIterator.getStartTime());
}

Animator.prototype.getMarkerTimeStamp = function () {
    var date = new Date(this.time);
    return new Intl.DateTimeFormat('fi-FI', {
        weekday: 'short',
        day: 'numeric',
        month: 'long',
        year: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        second: 'numeric',
        timeZoneName: 'short'
    }).format(date);
};

Animator.prototype.reInit = function (endtime) {
    if (this.time > endtime) {
        this.map.removeLayer(this.marker);
        this.map.clearLayers();
        this.pathIterator = new PathIterator(this.latlngs);
        this.timeBetweenFirstAndLast = this.pathIterator.getEndTime() - this.pathIterator.getStartTime();
        this.time = this.pathIterator.getStartTime();
        this.lastPosition = this.pathIterator.getPositionAtTime(this.time);
        this.markerPosition = this.lastPosition;
        this.marker = L.marker(this.markerPosition.toArray(), {zIndexOffset: 1000});
        this.marker.addTo(this.map);
        this.marker.bindPopup(this.getMarkerTimeStamp());
        this.paused = true;
    }

    while (this.time < endtime) {
        var timeStep = this.calculateTimeStep();
        this.lastPosition = this.markerPosition;
        this.markerPosition = this.pathIterator.getPositionAtTime(this.time);

        var polyline = L.polyline([this.lastPosition.toArray(), this.markerPosition.toArray()], {
            color: 'blue',
            opacity: 0.9
        });

        this.addNewPolyline(polyline);
        this.updatePolylines();

        this.time += timeStep;
    }
    this.marker.setLatLng(this.markerPosition.toArray());
    this.marker._popup.setContent(this.getMarkerTimeStamp());
};

//Animates the polylines and the marker on the map.
Animator.prototype.animate = function () {
    this.interval = setInterval(function () {

        var timeStep = this.calculateTimeStep();
        this.lastPosition = this.markerPosition;
        this.markerPosition = this.pathIterator.getPositionAtTime(this.time);

        var polyline = L.polyline([this.lastPosition.toArray(), this.markerPosition.toArray()], {
            color: 'blue',
            opacity: 0.9
        });

        this.addNewPolyline(polyline);
        this.updatePolylines();

        this.marker.setLatLng(this.markerPosition.toArray());
        this.marker._popup.setContent(this.getMarkerTimeStamp());
        setSliderValue(this.time);
        this.time += timeStep;
        if (this.time >= this.pathIterator.getEndTime()) clearTimeout(this.interval);
    }.bind(this), 100);
};

Animator.prototype.calculateTimeStep = function () {
    return $('#speedSlider').slider("option", "value") * this.timeBetweenFirstAndLast / 24000;
};

Animator.prototype.updatePolylines = function () {
    for (var j = 0; j < Math.min(this.polylines.length, 40); j++) {
        var line = this.polylines[j];

        var oldOpacity = line.options.opacity;
        var newOpacity = oldOpacity - 0.02;
        line.setStyle({color: 'blue', opacity: newOpacity});
    }
};

Animator.prototype.addNewPolyline = function (polyline) {
    if (this.polylines.length >= 40) {
        this.polyline.addLatLng(this.polylines[0].getLatLngs[1]);
        this.map.removeLayer(this.polylines[0]);
        this.polylines.shift();
    }
    polyline.addTo(this.map);
};


//Starts the animation.
Animator.prototype.start = function () {
    if (this.paused) {
        this.checkIfSelectedTimeIsBeforeCurrent();
        this.animate();
        this.paused = false;
        return true;
    }
};

Animator.prototype.checkIfSelectedTimeIsBeforeCurrent = function () {
    if ($("#playSlider").slider("option", "value") != this.time) {
        this.skipAnimationUntil();
    }
};

Animator.prototype.skipAnimationUntil = function () {
    if (this.paused) {
        this.reInit($("#playSlider").slider("option", "value"));
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
        return a.time - b.time;
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

setSliderValue = function (value) {
    var slider = $("#playSlider");
    slider.slider("option", "value", value);
};

//Initializes a slider with an attached label showing current value.
createSlider = function (min, max, step) {
    $("#playSlider").slider({
        min: min,
        max: max,
        step: step,
        change: function (event, ui) {
            var delay = function () {
                var label = '#playLabel';
                $(label).html(new Date(ui.value).toLocaleString()).position({
                    my: 'center top',
                    at: 'center bottom',
                    of: ui.handle
                }).css({visibility: 'visible'});
            };
            setTimeout(delay, 5);
        },
        slide: function (event, ui) {
            var delay = function () {
                var label = '#playLabel';
                $(label).html(new Date(ui.value).toLocaleString()).position({
                    my: 'center top',
                    at: 'center bottom',
                    of: ui.handle
                }).css({visibility: 'visible'});
            };
            setTimeout(delay, 5);
        }
    });
};
