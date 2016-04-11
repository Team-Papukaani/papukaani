function Player(map) {
    this.cslider = CanvasSlider("canvasslider", "ui-layer", "lines-layer", "background-layer");
    this.map = map;
    this.routes = [];
    this.animating = false;
    this.routeSplit = 100; // points per polyline. affects line stylechanges and backwardsreversing optimization
    this.slider = $("#playSlider");
    this.slider.slider({
        range: "min",
        min: 0,
        max: 9007199254740991,
        step: 1,
        paddingMin: 8,
        paddingMax: 8,
        slide: function (event, ui) {
            $('#playLabel').html(displayTime(ui.value * 1000));
            if (this.sliding) return;
            this.slider.slider("option", {
                value: ui.value
            });
            this.sliding = true;
            this.drawRoutes(true);
            this.sliding = false;
        }.bind(this),
        change: function (event, ui) {
            $('#playLabel').html(displayTime(ui.value * 1000));
        }
    });

    this.speedslider = $("#speedSlider");
    this.speedslider.slider({
        paddingMin: 8,
        paddingMax: 8,
        value: 250,
        min: 5,
        max: 100,
        change: function (event, ui) {
            if (this.runner) {
                clearInterval(this.runner);
                this.run();
            }
        }.bind(this)
    });
}

Player.prototype.addRoute = function (route) {
    if (route.points.length === 0) {
        this.cslider.add({
            id: route.individualId
        });
        return;
    }
    route.points.sort(function (a, b) {
        return new Date(a.d) - new Date(b.d);
    });
    if (route.points.length > 1) {
        var orig = route.points.slice(0);
        route.points = [];

        for (var i = 0, len = orig.length - 1; i < len; i++) {

            var pointA = orig[i];
            var pointB = orig[i + 1];

            route.points.push(pointA);

            // time in seconds between fake points
            var fillInterval = Math.max(360, 3 * (datetimestringToUnixtime(orig[orig.length - 1].d) - datetimestringToUnixtime(orig[0].d)) / 86400);
            var slice = parseFloat(datetimestringToUnixtime(pointB.d) - datetimestringToUnixtime(pointA.d)) / fillInterval;
            var directionVector = [pointB.x - pointA.x, pointB.y - pointA.y];
            var directionVectorScalar = 1 / slice;

            slice = Math.floor(slice);

            for (var j = 0; j < slice - 1; j++) {

                var time = new Date((datetimestringToUnixtime(pointA.d) + fillInterval) * 1000);
                var day = ('0' + time.getUTCDate()).slice(-2);
                var month = ('0' + (time.getUTCMonth() + 1)).slice(-2);
                var hours = ('0' + time.getUTCHours()).slice(-2);
                var minutes = ('0' + time.getUTCMinutes()).slice(-2);
                var seconds = ('0' + time.getUTCSeconds()).slice(-2);
                var year = time.getUTCFullYear();

                pointA = {
                    x: pointA.x + directionVector[0] * directionVectorScalar,
                    y: pointA.y + directionVector[1] * directionVectorScalar,
                    filler: true,
                    d: year + '-' + month + '-' + day + 'T' + hours + ':' + minutes + ':' + seconds + '+00:00'
                }
                route.points.push(pointA);
            }
        }
        route.points.push(orig[orig.length - 1]);
    }
    route.pointer = 0;
    route.featureGroup = L.featureGroup();
    route.featureGroup.addTo(this.map);
    route.lines = [L.polyline([], {color: route.color, opacity: 1, smoothFactor: 2, lineCap: "butt"})];
    route.lines[0].addTo(route.featureGroup);
    var p = route.points[route.pointer];
    route.marker = L.marker([p.x, p.y], {zIndexOffset: 1000});

    var lastPosition = route.points[route.points.length - 1];
    this.map.setView([lastPosition.x, lastPosition.y], 4);

    route.marker.addTo(route.featureGroup);
    route.marker.bindPopup(route.individualname + "<br>" +
        displayTime(route.points[route.pointer].d), {autoPan: false}).openPopup();
    route.marker.on("move", function (event) {
        route.marker.getPopup().setContent(route.individualname + "<br>" +
            displayTime(route.points[route.pointer].d));
    });
    this.routes.push(route);
    this.cslider.add({
        id: route.individualId,
        color: route.color,
        start: route.points[0].d,
        end: route.points[route.points.length - 1].d
    });
}

Player.prototype.removeRoute = function (route) {
    this.cslider.remove(route.individualId);
    var index = this.routes.indexOf(route);
    if (index >= 0) {
        this.routes.splice(index, 1);
        this.map.removeLayer(route.featureGroup);
        route.lines = [];
        this.refreshRoutes();
    }
    if (this.routes.length === 0) {
        this.stop();
    }
}

Player.prototype.stop = function () {
    clearInterval(this.runner);
    this.runner = undefined;
    this.animating = false;
    this.slider.slider("option", "value", this.slider.slider("option", "min"));
    $("#play").html("&#9658;");
    $('#playLabel').html("N/A");
    $('#playLabel_end').html("N/A");
}

Player.prototype.updateMinMax = function () {
    if (!this.routes.length) return;
    this.start = datetimestringToUnixtime(parseTime($("#start_time").val(), "+00:00"));
    this.end = datetimestringToUnixtime(parseTime($("#end_time").val(), "+00:00"));
    if (isNaN(this.start)) this.start = 0;
    if (isNaN(this.end)) this.end = 9007199254740991;
    var min = 9007199254740991;
    var max = 0;
    for (var i = 0; i < this.routes.length; i++) {
        min = Math.min(datetimestringToUnixtime(this.routes[i].points[0].d), min);
        max = Math.max(datetimestringToUnixtime(this.routes[i].points[this.routes[i].points.length - 1].d), max);
    }
    min = Math.max(min, this.start);
    max = Math.min(max, this.end);
    var options = {min: min, max: max};
    options.value = this.slider.slider("option", "value");
    if (options.value > max || options.value < min || !this.runner) {
        options.value = min;
    }
    this.slider.slider("option", options);
    $('#playLabel_end').html(displayTime(options.max * 1000));
    $('#playLabel').html(displayTime(options.value * 1000));

    this.cslider.draw(min, max);
}

Player.prototype.play = function () {
    if (this.routes.length === 0) {
        return;
    }
    if (this.runner) {
        clearInterval(this.runner);

        $("#play").html('<span class="glyphicon glyphicon-play"></span>');
        this.runner = undefined;
    } else {
        $("#play").html('<span class="glyphicon glyphicon-pause"></span>');
        var options = this.slider.slider("option");
        this.run();
    }
};

Player.prototype.run = function () {
    var that = this;
    this.runner = setInterval(function () {
        that.drawRoutes();
        var options = that.slider.slider("option");
        if (!that.animating) {
            that.play(); // pausee
            that.slider.slider("option", "value", options.max);
        } else {
            var step = Math.round((options.max - options.min) / 3000);
            step = Math.max(Math.min(step, options.max - options.value), 1);
            that.slider.slider("option", "value", options.value + step);
        }
    }, that.speedslider.slider("option", "max") - that.speedslider.slider("option", "value") + that.speedslider.slider("option", "min"));
}

Player.prototype.drawRoutes = function (animate) {
    var options = this.slider.slider("option");
    if (!this.runner && !animate) {
        options.value = options.max;
    }
    this.animating = false;

    for (var i = 0, len = this.routes.length; i < len; i++) {
        var route = this.routes[i];
        var newestPolylineIndex = route.lines.length - 1;
        var pointCount = route.points.length;
        if (pointCount <= route.pointer) continue;
        var point = route.points[route.pointer];
        var dateBegin = datetimestringToUnixtime(point.d);
        if (options.value > options.max) continue;
        this.animating = true;

        while (dateBegin > options.value && route.pointer > 0) {
            if (route.pointer % this.routeSplit === 0) {
                route.pointer -= this.routeSplit;
            } else {
                route.pointer -= route.pointer % this.routeSplit;
            }
            newestPolylineIndex--;
            if (route.pointer <= 0 || newestPolylineIndex < 0) {
                newestPolylineIndex = 0;
                route.pointer = 0;
            }
            route.featureGroup.removeLayer(route.lines.pop());

            point = route.points[route.pointer];
            dateBegin = datetimestringToUnixtime(point.d);
        }

        while (pointCount > route.pointer && dateBegin <= options.value) {
            var coordinates = [point.x, point.y];
            if (dateBegin >= options.min && dateBegin <= options.max) {
                if (route.pointer % this.routeSplit === 0) {
                    for (var r = newestPolylineIndex; r >= 0; r--) {
                        var opacity = 1 - (newestPolylineIndex - r + 1) * 0.1;
                        if (opacity < 0.3) break;
                        route.lines[r].setStyle({opacity: opacity});
                    }
                    route.lines[newestPolylineIndex].addLatLng(coordinates);
                    route.lines.push(L.polyline([], {
                        color: route.color,
                        opacity: 1,
                        smoothFactor: 2,
                        lineCap: "butt"
                    }));
                    route.lines[++newestPolylineIndex].addTo(route.featureGroup);
                }
                route.lines[newestPolylineIndex].addLatLng(coordinates);
            }
            route.pointer++;
            if (pointCount > route.pointer) {
                point = route.points[route.pointer];
                dateBegin = datetimestringToUnixtime(point.d);
            }
        }
        if (pointCount === route.pointer) route.pointer--;
        var p = route.points[route.pointer];
        var coordinates = [p.x, p.y];
        route.marker.setLatLng(coordinates);
    }
}

Player.prototype.clearRoute = function (route) {
    route.featureGroup.clearLayers();
    route.lines = [L.polyline([], {color: route.color, opacity: 1, smoothFactor: 2, lineCap: "butt"})];
    route.lines[0].addTo(route.featureGroup);
    route.pointer = 0;
    var p = route.points[route.pointer];
    var markerPosition = [p.x,p.y];
    route.marker.setLatLng(markerPosition);
    route.marker.addTo(route.featureGroup);
}

Player.prototype.refreshRoutes = function (animate) {
    this.updateMinMax();
    for (var i = 0, len = this.routes.length; i < len; i++) {
        this.clearRoute(this.routes[i]);
    }
    this.drawRoutes(animate);
}