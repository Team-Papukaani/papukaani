function Player(map) {
    this.map = map;
    this.routes = [];
    this.slider = new Slider();
}

Player.prototype.addRoute = function (route) {
    this.routes.push(route);
}

Player.prototype.removeRoute = function (route) {
    var index = this.routes.indexOf(route);
    if (index >= 0) {
        this.routes.splice(index, 1);
        this.map.removeLayer(route.lines);
    }
}

Player.prototype.showRoute = function (route) {
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

Player.prototype.drawRoutes = function () {
    // TODO: draws routes based on slider settings, minTime/maxTime etc.
}

function Slider() {
    // TODO: initialize slider
}



