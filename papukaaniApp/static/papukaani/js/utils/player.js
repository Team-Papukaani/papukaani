function Player(map) {
    this.map = map;
    this.routes = [];
    this.animating = false;
    this.routeSplit = 100; // points per polyline. affects line stylechanges and backwardsreversing optimization
    this.fillerDistance = 360; // time in seconds between fake points of data for smoother animation
    this.slider = $("#playSlider");
    this.slider.slider({
        range: "min",
        min: 0,
        max: 9007199254740991,
        step: 1,
        paddingMin: 8,
        paddingMax: 8,
        slide: function (event, ui) {
            $('#playLabel').html(new Date(ui.value * 1000).toLocaleString());
            if (this.sliding) return;
            this.slider.slider("option", {
                value: ui.value
            });
            this.sliding = true;
            this.drawRoutes(true);
            this.sliding = false;
        }.bind(this),
        change: function (event, ui) {
            $('#playLabel').html(new Date(ui.value * 1000).toLocaleString());
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
    if (route.points.length === 0) return;
    route.points.sort(function (a, b) {
        return new Date(a.dateBegin) - new Date(b.dateBegin);
    });
    if (route.points.length > 1) {
        var orig = route.points.slice(0);
        route.points = [];

        for (var i = 0, len = orig.length - 1; i < len; i++) {

            var pointA = orig[i];
            var pointB = orig[i + 1];

            route.points.push(pointA);

            var slice = parseFloat(datetimestringToUnixtime(pointB.dateBegin) - datetimestringToUnixtime(pointA.dateBegin)) / this.fillerDistance;
            var directionVector = [pointB.wgs84Geometry.coordinates[0] - pointA.wgs84Geometry.coordinates[0], pointB.wgs84Geometry.coordinates[1] - pointA.wgs84Geometry.coordinates[1]];
            var directionVectorScalar = 1 / slice;

            slice = Math.floor(slice);

            for (var j = 0; j < slice - 1; j++) {

                var time = new Date((datetimestringToUnixtime(pointA.dateBegin) + this.fillerDistance) * 1000);
                var day = ('0' + time.getUTCDate()).slice(-2);
                var month = ('0' + (time.getUTCMonth() + 1)).slice(-2);
                var hours = ('0' + time.getUTCHours()).slice(-2);
                var minutes = ('0' + time.getUTCMinutes()).slice(-2);
                var seconds = ('0' + time.getUTCSeconds()).slice(-2);
                var year = time.getUTCFullYear();

                pointA = {
                    wgs84Geometry: {coordinates: [pointA.wgs84Geometry.coordinates[0] + directionVector[0] * directionVectorScalar, pointA.wgs84Geometry.coordinates[1] + directionVector[1] * directionVectorScalar]},
                    filler: true,
                    dateBegin: year + '-' + month + '-' + day + 'T' + hours + ':' + minutes + ':' + seconds + '+00:00'
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

    var markerPosition = route.points[route.pointer].wgs84Geometry.coordinates;
    route.marker = L.marker([markerPosition[1], markerPosition[0]], {zIndexOffset: 1000});

    var lastPosition = route.points[route.points.length - 1].wgs84Geometry.coordinates;
    this.map.setView([lastPosition[1], lastPosition[0]], 4);

    route.marker.addTo(route.featureGroup);
    route.marker.bindPopup(route.individualname + "<br>" +
        new Date(route.points[route.pointer].dateBegin).toLocaleString(), {autoPan: false}).openPopup();
    route.marker.on("move", function (event) {
        route.marker.getPopup().setContent(route.individualname + "<br>" +
            new Date(route.points[route.pointer].dateBegin).toLocaleString());
    });


    this.routes.push(route);
}

Player.prototype.removeRoute = function (route) {
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
    if(!this.routes.length) return;
    this.start = datetimestringToUnixtime(parseTime($("#start_time").val(), "+00:00"));
    this.end = datetimestringToUnixtime(parseTime($("#end_time").val(), "+00:00"));
    if (isNaN(this.start)) this.start = 0;
    if (isNaN(this.end)) this.end = 9007199254740991;
    var min = 9007199254740991;
    var max = 0;
    for (var i = 0; i < this.routes.length; i++) {
        min = Math.min(datetimestringToUnixtime(this.routes[i].points[0].dateBegin), min);
        max = Math.max(datetimestringToUnixtime(this.routes[i].points[this.routes[i].points.length - 1].dateBegin), max);
    }
    min = Math.max(min, this.start);
    max = Math.min(max, this.end);
    var options = {min: min, max: max};
    options.value = this.slider.slider("option", "value");
    if (options.value > max || options.value < min || !this.runner) {
        options.value = min;
    }
    this.slider.slider("option", options);
    $('#playLabel_end').html(new Date(options.max * 1000).toLocaleString());
    $('#playLabel').html(new Date(options.value * 1000).toLocaleString());
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
        var dateBegin = datetimestringToUnixtime(point.dateBegin);
        if (options.value > options.max) continue;
        this.animating = true;

        while (dateBegin > options.value) {
            if (route.pointer % this.routeSplit === 0) {
                route.pointer -= this.routeSplit;
            } else {
                route.pointer -= route.pointer % this.routeSplit;
            }
            newestPolylineIndex--;
            if (route.pointer <= 0 || newestPolylineIndex < 0) {
                this.clearRoute(route);
                newestPolylineIndex = 0;
                route.pointer = 0;
                break;
            }
            route.featureGroup.removeLayer(route.lines.pop());

            point = route.points[route.pointer];
            dateBegin = datetimestringToUnixtime(point.dateBegin);
        }

        while (pointCount > route.pointer && dateBegin <= options.value) {
            var coordinates = point.wgs84Geometry.coordinates;
            if (dateBegin >= options.min && dateBegin <= options.max) {
                if (route.pointer % this.routeSplit === 0) {
                    for (var r = newestPolylineIndex; r >= 0; r--) {
                        var opacity = 1 - (newestPolylineIndex - r + 1) * 0.1;
                        if (opacity < 0.3) break;
                        route.lines[r].setStyle({opacity: opacity});
                    }
                    route.lines[newestPolylineIndex].addLatLng([coordinates[1], coordinates[0]]);
                    route.lines.push(L.polyline([], {
                        color: route.color,
                        opacity: 1,
                        smoothFactor: 2,
                        lineCap: "butt"
                    }));
                    route.lines[++newestPolylineIndex].addTo(route.featureGroup);
                }
                route.lines[newestPolylineIndex].addLatLng([coordinates[1], coordinates[0]]);
            }
            route.pointer++;
            if (pointCount > route.pointer) {
                point = route.points[route.pointer];
                dateBegin = datetimestringToUnixtime(point.dateBegin);
            }
        }
        if (pointCount === route.pointer) route.pointer--;
        var coordinates = route.points[route.pointer].wgs84Geometry.coordinates;
        route.marker.setLatLng([coordinates[1], coordinates[0]]);
    }
}

Player.prototype.clearRoute = function (route) {
    route.featureGroup.clearLayers();
    route.lines = [L.polyline([], {color: route.color, opacity: 1, smoothFactor: 2, lineCap: "butt"})];
    route.lines[0].addTo(route.featureGroup);
    route.pointer = 0;
    var markerPosition = route.points[route.pointer].wgs84Geometry.coordinates;
    route.marker.setLatLng([markerPosition[1], markerPosition[0]]);
    route.marker.addTo(route.featureGroup);
}

Player.prototype.refreshRoutes = function (animate) {
    this.updateMinMax();
    for (var i = 0, len = this.routes.length; i < len; i++) {
        this.clearRoute(this.routes[i]);
    }
    this.drawRoutes(animate);
}