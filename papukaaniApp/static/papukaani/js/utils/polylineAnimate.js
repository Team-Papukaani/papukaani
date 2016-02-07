function Animator(latlngs, individualname, map, color) {
    this.color = color;
    this.map = map;
    this.latlngs = latlngs;
    this.individual = individualname;
    this.initializePathIterator();
    this.initializeMarker();
    this.initializePolyLines();
    this.initializeSlider();

}

//Initializes the PathIterator and its variables.
Animator.prototype.initializePathIterator = function () {
    this.pathIterator = new PathIterator(this.latlngs);
    this.timeBetweenFirstAndLast = this.pathIterator.getEndTime() - this.pathIterator.getStartTime();
    this.time = this.pathIterator.getStartTime();
    this.lastPosition = this.pathIterator.getPositionAtTime(this.time);
    this.markerPosition = this.lastPosition;
};

//Initializes the slider and its variables.
Animator.prototype.initializeSlider = function () {
    this.createSlider(this.pathIterator.getStartTime(), this.pathIterator.getEndTime(), 1);
    $("#playLabel_end").text(new Date(this.pathIterator.getEndTime()).toLocaleString());
    this.setSliderValue(this.pathIterator.getStartTime());
    this.sliderBeingMovedByUser = false;
    this.paused = true;
};

//Initializes the marker and its popup and adds them to the map.
Animator.prototype.initializeMarker = function () {
    this.marker = L.marker(this.markerPosition.toArray(), {zIndexOffset: 1000});
    this.marker.addTo(this.map);
    this.marker.bindPopup(this.popupContent(), {autoPan: false});
};

//Initializes polyline components and adds the master polyline to the map.
Animator.prototype.initializePolyLines = function () {
    this.polylines = [];
    //Default options for the main polyline.
    var polylineOptions = {color: this.color, opacity: 0.3, smoothFactor: 0};
    this.polyline = L.polyline([], polylineOptions);
    this.polyline.addTo(this.map);
};

//Returns the point's timestamp(ms) in locale-specific format.
Animator.prototype.getMarkerTimeStamp = function () {
    var date = new Date(this.time);
    return date.toLocaleString();
};

//Content for the marker's popup.
Animator.prototype.popupContent = function () {
    return this.individual + "<br>" + this.getMarkerTimeStamp();
};

//Updates the marker's position and popup content.
Animator.prototype.updateMarker = function () {
    this.marker.setLatLng(this.markerPosition.toArray());
    this.marker._popup.setContent(this.popupContent());
};

//Updates the marker location and popup content, and the slider's value.
Animator.prototype.updateMarkerAndSlider = function () {
    this.updateMarker();
    this.setSliderValue(this.time);
};

//Changes the animator's state to match the specified time, in effect skipping the animation until the correct time is reached.
Animator.prototype.reInit = function (endtime) {
    var oldSpeed = $("#speedSlider").slider("option", "value");
    $("#speedSlider").slider("option", "value", 50);
    if (this.time > endtime) {
        this.map.clearLayers();
        this.initializePolyLines();
        this.initializePathIterator();
        this.updateMarker();
        this.paused = true;
    }

    while (this.time < endtime) {
        this.drawPath(false);
    }
    this.updateMarker();
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
        this.drawPathEnd(animated);
    }
};

//Draws the final polyline when time exceeds or equals PathIterator's getEndTime.
Animator.prototype.drawPathEnd = function (animated) {
    this.time = this.pathIterator.getEndTime();
    this.lastPosition = this.markerPosition;
    this.markerPosition = this.pathIterator.getLastPoint().coordinates;

    var polyline = this.newPolyline();

    this.addNewPolyline(polyline);
    this.updatePolylines();

    if (animated) {
        this.updateMarkerAndSlider();
    }
};

//New polyline with default settings.
Animator.prototype.newPolyline = function () {
    return L.polyline([this.lastPosition.toArray(), this.markerPosition.toArray()], {
        color: this.color,
        opacity: 1.0
    });
};

//Determines how fast the animation progresses, based on speedSlider value and actual time-range of points.
Animator.prototype.calculateTimeStep = function () {
    return $('#speedSlider').slider("option", "value") * this.timeBetweenFirstAndLast / 24000;
};

//Decreases opacity of polylines as distance to head grows, until the polyline is far enough.
Animator.prototype.updatePolylines = function () {
    /* for (var j = 0; j < Math.min(this.polylines.length, 20); j++) {
     var line = this.polylines[j];

     var oldOpacity = line.options.opacity;
     var newOpacity = oldOpacity - 0.03;
     line.setStyle({color: this.color, opacity: newOpacity});
     }*/
};

//Adds a new polyline to the map, and if numerous enough merges one from the tail to the master polyline to maintain performance.
Animator.prototype.addNewPolyline = function (polyline) {
    this.polylines.push(polyline);
    /*if (this.polylines.length >= 20) {
     this.polyline.addLatLng(this.polylines[0].getLatLngs()[1]);
     this.map.removeLayer(this.polylines[0]);
     this.polylines.shift();
     }*/
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

//Forwards the animation until max time is reached.
Animator.prototype.forwardToEnd = function () {
    var slider = $("#playSlider");
    var max = slider.slider("option", "max");
    this.reInit(max);
    this.marker.openPopup();
    this.animationComplete = true;
    $("#play").html("&#9658;");
};

//Removes the animation, effectively removing all markers and polylines created by it.
Animator.prototype.clear = function () {
    this.stop();
    this.map.removeLayer(this.marker);
    this.map.clearLayers();
    if (sorter.getRoutes().length == 1) {
        $("#playSlider").slider("destroy");
        createDummySlider();
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
        if (time < this.getStartTime()) {
            return null;
        }
        while (currentIndex < orderedPoints.length - 1 && time >= orderedPoints[currentIndex + 1].time) {
            currentIndex++;
        }
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

//Initializes a slider with an attached label showing current value.
Animator.prototype.createSlider = function (min, max, step) {
    if (sorter.getRoutes().length > 1) {
        min = Math.min($("#playSlider").slider("option", "min"), min);
        $("#playSlider").slider("option", "min", min);
        max = Math.max($("#playSlider").slider("option", "max"), max);
        $("#playSlider").slider("option", "max", max);
        $("#playLabel_end").text(new Date(max).toLocaleString());
        this.setSliderValue(min);
        return;
    }
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
            var cont = false;
            if (this.stop()) {
                cont = true;
            }
            this.reInit(ui.value);
            if (cont) {
                this.start();
            }
            this.sliderBeingMovedByUser = false;
        }, 250).bind(this)
    });
};

//Sets the slider to the desired value, unless it is currently being moved by the user.
Animator.prototype.setSliderValue = function (value) {
    if (!this.sliderBeingMovedByUser) {
        var slider = $("#playSlider");
        slider.slider("option", "value", value);
    }
};

//Prevents function from being called too quickly in succession.
function debounce(func, wait, immediate) {
    var timeout;
    return function () {
        var context = this, args = arguments;
        var later = function () {
            timeout = null;
            if (!immediate) {
                func.apply(context, args);
            }
        };
        var callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) {
            func.apply(context, args);
        }
    };
}

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