function Slider(loc,zoom) {
    this.map = create_map("map",loc,zoom);
    this.routes = [];
}

Slider.prototype.addRoute = function(route) {
    this.routes.push(route);
}

Slider.prototype.drawRoute = function (route) {
    var featureGroup = L.featureGroup();
    var map = this.map;
    featureGroup.addTo(map);
    var reitti = L.polyline([], {color: "red"}).addTo(featureGroup);

    $.get("../rest/gatheringsForIndividual?individualId=" + 54334 + "&format=json", {}, function(data){

        var name = data.pop();

        data.sort(function (a, b) {
            return new Date(a.dateBegin) - new Date(b.dateBegin);
        });

        _draw(data);


    }, "json");

    function _draw(data) {

        var a = setInterval(function(){
            var p = data.shift()
            if (data.length == 0) {
                clearInterval(a);
            }
            reitti.addLatLng([p.wgs84Geometry.coordinates[1], p.wgs84Geometry.coordinates[0]]);
        }, 100);
    }

}
