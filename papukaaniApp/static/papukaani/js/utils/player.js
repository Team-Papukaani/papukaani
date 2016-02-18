function Player(map) {
    this.map = map;
    this.routes = [];
    this.slider = new Slider();
}

Player.prototype.addRoute = function (route) {
    route.points.sort(function (a, b) {
        return new Date(a.dateBegin) - new Date(b.dateBegin);
    });
    this.routes.push(route);
}

Player.prototype.removeRoute = function (route) {
    var index = this.routes.indexOf(route);
    if (index >= 0) {
        this.routes.splice(index, 1);
        this.map.removeLayer(route.lines);
        route.lines = null;
    }
}

Player.prototype.showRoute = function (route) {
    var map = this.map;
    var featureGroup = L.featureGroup();
    featureGroup.addTo(map);
    route.lines = L.polyline([], {color: route.color});
    route.lines.addTo(featureGroup);

    var start = $("#start_time").val();
    var end = $("#end_time").val();

    var points = route.points;
    if (start !== "" || end !== "") {
        points = points_in_timerange(route.points, start, end);
    }

    for (var i in points) {
        route.lines.addLatLng([points[i].wgs84Geometry.coordinates[1], points[i].wgs84Geometry.coordinates[0]]);
    }
}

Player.prototype.drawRoutes = function () {
    // TODO: draws routes based on slider settings, minTime/maxTime etc.
    var map = this.map;
    var featureGroup = L.featureGroup();
    featureGroup.addTo(map);
    route.lines = L.polyline([], {color: route.color});
    route.lines.addTo(featureGroup);

    route.points.sort(function (a, b) {
        return new Date(a.dateBegin) - new Date(b.dateBegin);
    });

    var points = route.points.slice(0);
    if (points.length == 0) return;

    var a = setInterval(function(){
        var point = points.shift();
        if (points.length == 0) {
            clearInterval(a);
        }
        route.lines.addLatLng([point.wgs84Geometry.coordinates[1], point.wgs84Geometry.coordinates[0]]);
    }, 10);
}

Player.prototype.refreshRoutes = function () {
    for (var i in this.routes) {
        this.map.removeLayer(this.routes[i].lines);
        this.routes[i].lines = null;
        this.showRoute(this.routes[i]);
    }
}

function Slider() {
    // TODO: initialize slider
}



