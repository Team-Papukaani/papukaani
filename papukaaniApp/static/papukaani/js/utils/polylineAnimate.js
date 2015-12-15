function Animator(latlngs, individualname, map) {
    this.map = map;
    this.latlngs = latlngs;
    this.individual = individualname;
    this.pathIterator = new PathIterator(latlngs);
    this.polylines = [];
    this.timeBetweenFirstAndLast = this.pathIterator.getEndTime() - this.pathIterator.getStartTime();
    this.time = this.pathIterator.getStartTime();
    this.lastPosition = this.pathIterator.getPositionAtTime(this.time);
    this.markerPosition = this.lastPosition;
    this.marker = L.marker(this.markerPosition.toArray(), {zIndexOffset: 1000});
    this.marker.addTo(this.map);
    this.marker.bindPopup(this.getMarkerTimeStamp());
    this.polyline = L.polyline([], polylineOptions);
    this.polyline.addTo(this.map);
    this.paused = true;
    this.createSlider(this.pathIterator.getStartTime(), this.pathIterator.getEndTime(), 1);
    $("#playLabel_end").text(new Date(this.pathIterator.getEndTime()).toLocaleString());
    this.setSliderValue(this.pathIterator.getStartTime());
    this.sliderBeingMovedByUser = false;
}

//Default options for the main polyline.
var polylineOptions = {color: 'blue', opacity: 0.3, smoothFactor: 0};

//Returns the points timestamp(ms) in the specified datetime format.
Animator.prototype.getMarkerTimeStamp = function () {
    var date = new Date(this.time);
    /*return new Intl.DateTimeFormat('fi-FI', {
     weekday: 'short',
     day: 'numeric',
     month: 'long',
     year: 'numeric',
     hour: 'numeric',
     minute: 'numeric',
     second: 'numeric',
     timeZoneName: 'short'
     }).format(date);*/
    return date.toLocaleString()
};

Animator.prototype.popupContent = function () {
    return this.individual + "<br>" + this.getMarkerTimeStamp();
};

//Changes the animator's state to match the specified time, in effect skipping the animation until the correct time is reached.
Animator.prototype.reInit = function (endtime) {
    var oldSpeed = $("#speedSlider").slider("option", "value");
    $("#speedSlider").slider("option", "value", 50);
    if (this.time > endtime) {
        this.map.removeLayer(this.marker);
        this.map.clearLayers();
        this.polylines = [];
        this.pathIterator = new PathIterator(this.latlngs);
        this.timeBetweenFirstAndLast = this.pathIterator.getEndTime() - this.pathIterator.getStartTime();
        this.time = this.pathIterator.getStartTime();
        this.lastPosition = this.pathIterator.getPositionAtTime(this.time);
        this.markerPosition = this.lastPosition;
        this.marker = L.marker(this.markerPosition.toArray(), {zIndexOffset: 1000});
        this.marker.addTo(this.map);
        this.marker.bindPopup(this.getMarkerTimeStamp());
        this.polyline = L.polyline([], polylineOptions);
        this.polyline.addTo(this.map);
        this.paused = true;
    }

    while (this.time < endtime) {
        this.drawPath(false);
    }
    this.marker.setLatLng(this.markerPosition.toArray());
    this.marker._popup.setContent(this.popupContent());
    $("#speedSlider").slider("option", "value", oldSpeed);
};

//Begins animation of polyline drawing and marker movement.
Animator.prototype.animate = function () {
    this.interval = setInterval(function () {
        this.drawPath(true);
        if (this.time >= this.pathIterator.getEndTime()) {
            this.setSliderValue(this.pathIterator.getEndTime());
            this.animationComplete = true;
            this.stop();
            animationEnd();
        }
    }.bind(this), 100);
};

//Draws a polyline, with animation if parameter is true.
Animator.prototype.drawPath = function (animated) {
    var timeStep = this.calculateTimeStep();
    this.lastPosition = this.markerPosition;
    this.markerPosition = this.pathIterator.getPositionAtTime(this.time);

    var polyline = this.newPolyline();

    this.addNewPolyline(polyline);
    this.updatePolylines();

    if (animated) {
        this.updateMarkerAndSlider();
    }
    this.time += timeStep;
    if (this.time >= this.pathIterator.getEndTime()) {
        this.time = this.pathIterator.getEndTime();
        this.lastPosition = this.markerPosition;
        this.markerPosition = this.pathIterator.getLastPoint().coordinates;

        var polyline = this.newPolyline();

        this.addNewPolyline(polyline);
        this.updatePolylines();

        if (animated) {
            this.updateMarkerAndSlider();
        }
    }
};

//Updates the marker location and popup content, and the slider's value.
Animator.prototype.updateMarkerAndSlider = function () {
    this.marker.setLatLng(this.markerPosition.toArray());
    this.marker._popup.setContent(this.popupContent());
    this.setSliderValue(this.time);
};

//New polyline with default settings.
Animator.prototype.newPolyline = function () {
    return L.polyline([this.lastPosition.toArray(), this.markerPosition.toArray()], {
        color: 'blue',
        opacity: 1.0
    });
};

Animator.prototype.calculateTimeStep = function () {
    return $('#speedSlider').slider("option", "value") * this.timeBetweenFirstAndLast / 24000;
};

//Decreases opacity of polylines as distance to head grows, until the polyline is far enough.
Animator.prototype.updatePolylines = function () {
    for (var j = 0; j < Math.min(this.polylines.length, 20); j++) {
        var line = this.polylines[j];

        var oldOpacity = line.options.opacity;
        var newOpacity = oldOpacity - 0.03;
        line.setStyle({color: 'blue', opacity: newOpacity});
    }
};

//Adds a new polyline to the map, and if numerous enough merges one from the tail to the master polyline to maintain performance.
Animator.prototype.addNewPolyline = function (polyline) {
    this.polylines.push(polyline);
    if (this.polylines.length >= 20) {
        this.polyline.addLatLng(this.polylines[0].getLatLngs()[1]);
        this.map.removeLayer(this.polylines[0]);
        this.polylines.shift();
    }
    polyline.addTo(this.map);
};

//Starts (or continues) the animation.
Animator.prototype.start = function () {
    if (this.animationComplete) {
        this.startFromBeginning();
        this.animationComplete = false;
    }
    if (this.paused) {
        this.animate();
        this.paused = false;
        return true;
    }
};

//Initializes the animation to the starting point.
Animator.prototype.startFromBeginning = function () {
    var min = $("#playSlider").slider("option", "min");
    this.reInit(min);
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
        if (points.length > 1) {
            var pointAIndex = this.getPointIndexAtTime(time);
            var pointA = points[pointAIndex];
            var pointB = points[pointAIndex + 1];

            if (pointB === undefined) {
                pointB = pointA;
            }

            var directionVector = pointB.coordinates.clone().subtract(pointA.coordinates);
            var timeSincePointA = time - pointA.time;
            var pointTimeDifference = pointB.time - pointA.time;
            var directionVectorScalar = timeSincePointA / pointTimeDifference;
            return pointA.coordinates.clone().add(directionVector.multiplyScalar(directionVectorScalar));
        } else {
            return points[0].coordinates.clone();
        }
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

    this.getLastPoint = function () {
        return orderedPoints[orderedPoints.length - 1];
    };
};

//Removes the animation, effectively removing all markers and polylines created by it.
Animator.prototype.clear = function () {
    this.stop();
    this.map.removeLayer(this.marker);
    this.map.clearLayers();
    createDummySlider();
};

//Adds clearLayers function, which removes all polylines, to Map.
L.Map.include({
    'clearLayers': function () {
        this.eachLayer(function (layer) {
            if ("_container" in layer) {
                if (layer._container.toString().indexOf("SVGG") > -1) {
                    this.removeLayer(layer);
                }
            }
        }, this);
    }
});

//Sets the slider to the desired value, unless it is currently being moved by the user.
Animator.prototype.setSliderValue = function (value) {
    if (!this.sliderBeingMovedByUser) {
        var slider = $("#playSlider");
        slider.slider("option", "value", value);
    }
};

//Initializes a slider with an attached label showing current value.
Animator.prototype.createSlider = function (min, max, step) {
    $("#playSlider").slider({
        range: "min",
        min: min,
        max: max,
        step: step,
        paddingMin: 7,
        paddingMax: 7,
        //Change the label value to match when slider value changed by animation.
        change: function (event, ui) {
            var label = '#playLabel';
            $(label).html(new Date(ui.value).toLocaleString());
        },
        //When moving the slider, the value and label will only be changed by user actions, not by the animation.
        slide: function (event, ui) {
            this.sliderBeingMovedByUser = true;
            this.animationComplete = false;
            var delay = function () {
                var label = '#playLabel';
                $(label).html(new Date(ui.value).toLocaleString());
            };
            setTimeout(delay, 5);
        }.bind(this),
        // When the user stops moving the slider,
        // the animation will advance to the point indicated by the slider and continue playing if applicable.
        // Slider and label value will return to being controlled by the animation.
        // Uses debounce to prevent event stacking and slowdown.
        stop: debounce(function (event, ui) {
            if (this.stop()) var cont = true;
            this.reInit(ui.value);
            if (cont) this.start();
            this.sliderBeingMovedByUser = false;
        }, 250).bind(this)
    });
};

//Prevents function from being called too quickly in succession.
function debounce(func, wait, immediate) {
    var timeout;
    return function () {
        var context = this, args = arguments;
        var later = function () {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        var callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}

//Forwards the animation until max time is reached.
Animator.prototype.forwardToEnd = function () {
    var slider = $("#playSlider");
    var max = slider.slider("option", "max");
    this.reInit(max);
    this.marker.openPopup();
    this.animationComplete = true;
};