
function init(docs){
    sorter = new DeviceSorter(docs)
    map = new PublicMap(sorter.points)

    sorter.setMap(map)
}

function PublicMap(points){
    this.map = create_map("map", [61.0, 20.0], 5);

    this.draw(points)

    this.map.fitBounds(this.arrow.getBounds());
}

//Draws the polyline
PublicMap.prototype.draw = function(points){
    var latlngs = this.createLatlngsFromPoints(points);

    // --- Arrow, with animation to demonstrate the use of setPatterns ---
    this.arrow = L.polyline(latlngs, {color: 'blue', dashArray: '20,15', smoothFactor:50.0}).addTo(this.map);
    if(points.length > 1){
        this.arrowHead = L.polylineDecorator(this.arrow).addTo(this.map);

        var arrowOffset = 0;
        var anim = window.setInterval(function() {
            this.arrowHead.setPatterns([
                {offset: arrowOffset+'%', repeat: 0, symbol: L.Symbol.arrowHead({pixelSize: 15, polygon: false, pathOptions: {stroke: true}})}
            ])
            if(++arrowOffset > 100)
                arrowOffset = 0;
        }.bind(this), 100);
    }
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