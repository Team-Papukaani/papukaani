
function init(devices){
    sorter = new DeviceSorter(devices)
    map = new PublicMap(sorter.points)

    sorter.setMap(map)
}

function PublicMap(points){
    this.map = create_map("map", [61.0, 20.0], 5);

    this.draw(points)

}

//Draws the polyline
PublicMap.prototype.draw = function(points){
    var latlngs = this.createLatlngsFromPoints(points);

    polylines = []
    i = 0;
    window.setInterval(function() {
        polyline = L.polyline([latlngs[i], latlngs[++i]], {color: 'blue', opacity: 1.0})
        polylines.push(polyline)
        polyline.addTo(this.map);
        this.map.panTo(latlngs[i])
        if(polylines.length > 15) {
            polylines.splice(0, 1);
        }
        for(j=0; j < polylines.length; j++) {
            polylines[j].setStyle({color: 'blue', opacity: (j/15.0)});
        }
    }.bind(this), 700);

}
//Redraws the polyline
PublicMap.prototype.changePoints = function(points){
    this.map.removeLayer(this.arrow)
    this.map.removeLayer(this.arrowHead)

    this.draw(points)
}

//Creates latLng objects from points
PublicMap.prototype.createLatlngsFromPoints = function(points){
    var latlngs = [];
    for(var i = 0; i < points.length; i++){
        var coordinates = points[i].wgs84Geometry.coordinates;
        var latlng = L.latLng(coordinates[1], coordinates[0]);
        latlngs.push(latlng);
    }
    return latlngs;
}