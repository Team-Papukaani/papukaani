function Player(map) {
    this.map = map;
    this.routes = [];
    this.animating = false;

    this.slider = $("#playSlider");
    this.slider.slider({
        range: "min",
        min: 0,
        max: 9007199254740991,
        step: 1,
        paddingMin: 7,
        paddingMax: 7,

        slide: function (event, ui) {
            if (this.runner) {
                clearInterval(this.runner);
            }
            this.refreshRoutes(true);
            this.drawRoutes();
            if (this.runner) {
                this.run();
            }
        }.bind(this),
        change: function (event, ui) {
            $('#playLabel').html(new Date(ui.value * 1000).toLocaleString());
        }
    });

    this.speedslider = $("#speedSlider");
    this.speedslider.slider({
        value: 500,
        min: 50,
        max: 1000,
        slide: function (event, ui) {
            clearInterval(this.runner);
            this.run();
        }.bind(this)
    });
}

Player.prototype.addRoute = function (route) {
    if (route.points.length === 0) return;
    route.points.sort(function (a, b) {
        return new Date(a.dateBegin) - new Date(b.dateBegin);
    });
    route.pointer = 0;

    route.featureGroup = L.featureGroup();
    route.featureGroup.addTo(this.map);
    route.lines = L.polyline([], {color: route.color});
    route.lines.addTo(route.featureGroup);

    var markerPosition = route.points[route.pointer].wgs84Geometry.coordinates;
    route.marker = L.marker([markerPosition[1], markerPosition[0]], {zIndexOffset: 1000});
    route.featureGroup.addLayer(route.marker);
    route.marker.bindPopup(route.individualname + "<br>" +
        new Date(route.points[route.pointer].dateBegin).toLocaleString(), {autoPan: false}).openPopup();
    route.marker.on("move", function (event) {
        route.marker.getPopup().setContent(route.individualname + "<br>" +
            new Date(route.points[route.pointer].dateBegin).toLocaleString());
    });

    this.routes.push(route);
    this.updateMinMax();
}

Player.prototype.removeRoute = function (route) {
    var index = this.routes.indexOf(route);
    if (index >= 0) {
        this.routes.splice(index, 1);
        this.map.removeLayer(route.featureGroup);
        route.lines = null;
        this.updateMinMax();
    }
    if (this.routes.length === 0) {
        this.stop();
    }
}

Player.prototype.stop = function () {
    clearInterval(this.runner);
    this.runner = undefined;
    this.animating = false;
    this.updateMinMax();
    this.slider.slider("option", "value", this.slider.slider("option", "min"));
    $("#play").html("&#9658;");
    $('#playLabel').html("N/A");
}

Player.prototype.refreshTimeBounds = function () {
    this.start = datetimestringToUnixtime(parseTime($("#start_time").val(), "+00:00"));
    this.end = datetimestringToUnixtime(parseTime($("#end_time").val(), "+00:00"));
    if (isNaN(this.start)) this.start = 0;
    if (isNaN(this.end)) this.end = 9007199254740991;
}

Player.prototype.updateMinMax = function () {
    var min = 9007199254740991;
    var max = 0;
    this.refreshTimeBounds();
    for (var i = 0; i < this.routes.length; i++) {
        min = Math.min(datetimestringToUnixtime(this.routes[i].points[0].dateBegin), min);
        max = Math.max(datetimestringToUnixtime(this.routes[i].points[this.routes[i].points.length - 1].dateBegin), max);
    }
    min = (this.start < min) ? min : this.start;
    max = (this.end > max) ? max : this.end;

    var options = {min: min, max: max};
    options.value = this.slider.slider("option", "value");
    if (options.value > max || options.value < min) {
        options.value = min;
    }
    this.slider.slider("option", options);
    $('#playLabel').html(new Date(options.value * 1000).toLocaleString());
}

Player.prototype.play = function () {
    if (this.routes.length === 0) {
        this.stop();
        return;
    }
    if (this.runner) {
        clearInterval(this.runner);
        $("#play").html("&#9658;");
        this.runner = undefined;
    } else {
        $("#play").html("&#9646;&#9646;");
        this.refreshRoutes(true);
        this.refreshTimeBounds();
        this.drawRoutes();
        this.run();
    }
};

Player.prototype.run = function () {
    var that = this;
    this.runner = setInterval(function () {
        that.drawRoutes();
        if (!that.animating) {
            clearInterval(that.runner);
        } else {
            var step = Math.round((that.slider.slider("option", "max") - that.slider.slider("option", "min")) / 300);
            that.slider.slider("option", "value", that.slider.slider("option", "value") + step);
        }
    }, that.speedslider.slider("option", "max") - that.speedslider.slider("option", "value") + that.speedslider.slider("option", "min"));
}

Player.prototype.drawRoutes = function () {
    var options = this.slider.slider("option");
    this.animating = false;

    for (var i = 0, len = this.routes.length; i < len; i++) {
        var route = this.routes[i];
        var pointcount = route.points.length;
        if (pointcount <= route.pointer) continue;
        this.animating = true;
        var point = route.points[route.pointer];
        var dateBegin = datetimestringToUnixtime(point.dateBegin);
        while (pointcount > route.pointer && dateBegin <= options.value) {
            var coordinates = point.wgs84Geometry.coordinates;
            if (dateBegin >= options.min && dateBegin <= options.max) {
                route.lines.addLatLng([coordinates[1], coordinates[0]]);
                route.marker.setLatLng([coordinates[1], coordinates[0]]);
            }
            route.pointer++;
            if (pointcount > route.pointer) {
                point = route.points[route.pointer];
                dateBegin = datetimestringToUnixtime(point.dateBegin);
            }
        }
    }
}

Player.prototype.clearRoute = function (route) {
    route.featureGroup.clearLayers();
    route.lines = L.polyline([], {color: route.color});
    route.lines.addTo(route.featureGroup);
    route.pointer = 0;
    if (route.marker) {
        var markerPosition = route.points[route.pointer].wgs84Geometry.coordinates;
        route.marker.setLatLng([markerPosition[1], markerPosition[0]]);
        route.featureGroup.addLayer(route.marker);
        route.marker.openPopup();
    }
}

Player.prototype.refreshRoutes = function (animation) {
    for (var i = 0, len = this.routes.length; i < len; i++) {
        this.clearRoute(this.routes[i]);
    }
    this.drawRoutes();
}