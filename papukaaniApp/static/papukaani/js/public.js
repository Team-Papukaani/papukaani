function init(devices) {
    this.sorter = new DeviceSorter(devices);
    map = new PublicMap(sorter.points);

    sorter.setMap(map)
}

function PublicMap() {
    this.map = create_map("map", [61.0, 20.0], 5);
}

//Draws the polyline
PublicMap.prototype.draw = function (points) {
    doc = points[0];
    pi = new PathIterator(doc.gatherings);
    polylines = [];
    time = pi.getStartTime();

    i = 0;
    window.setInterval(function () {
        polyline = L.polyline([latlngs[i], latlngs[++i]], {color: 'blue', opacity: 1.0})
        polylines.push(polyline);
        polyline.addTo(this.map);
        this.map.panTo(latlngs[i]);
        if (polylines.length > 15) {
            polylines.splice(0, 1);
        }
        for (j = 0; j < polylines.length; j++) {
            polylines[j].setStyle({color: 'blue', opacity: (j / 15.0)});
        }
    }.bind(this), 700);

};


function pointsToLatLngTime(points) {
    return points.map(function(point) {
        return {
            lat: point.wgs84Geometry.coordinates[1],
            lng: point.wgs84Geometry.coordinates[0],
            time: Date.parse(point.timeStart)
        };
    });
}

var PathIterator = function(points) {
    var latLngTimes = pointsToLatLngTime(points);
    var orderedPoints = latLngTimes.sort(function(a, b) {
        return a.time - b.time
    });
    var currentIndex = 0;
    this.getPointAtTime = function(time) {
        while(time > orderedPoints[currentIndex+1].time) currentIndex++;
        return orderedPoints[currentIndex];
    }

    this.getStartTime = function() {
        return orderedPoints[0].time;
    }
}

//Redraws the polyline
PublicMap.prototype.changePoints = function (points) {
    this.draw(points)
};

//Creates latLng objects from points
PublicMap.prototype.createLatlngsFromPoints = function (points) {
    var latlngs = [];
    for (var p = 0; p < points.length; p++) {
        for (var i = 0; i < points[p]["gatherings"].length; i++) {
            var ltlgs = points[p]["gatherings"][i].wgs84Geometry.coordinates;
            latlngs.push([ltlgs[1], ltlgs[0]]);
        }
    }
    return latlngs;
};

//Disables the select, save and reset buttons.
function lockButtons() {
    $("#selectDevice").attr("disabled", true);
}

//Enables the select, save and reset buttons.
function unlockButtons() {
    $("#selectDevice").attr("disabled", false);
}