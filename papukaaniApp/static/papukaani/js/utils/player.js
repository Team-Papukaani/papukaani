function Player(map) {
    this.map = map;
    this.routes = [];
    this.slider = $("#playSlider");
    this.slider.slider({
        range: "min",
        min: 0,
        max: Number.MAX_VALUE,
        step: 1,
        paddingMin: 7,
        paddingMax: 7,

        slide:function(event,ui){
            if (this.runner) {
                clearInterval(this.runner);
            }
            this.refreshRoutes(true);
            this.drawRoutes();
            if (this.runner) {
                this.run();
            }
        }.bind(this),

        //Change the label value to match when slider value changed by animation.
        change: function (event, ui) {
            $('#playLabel').html(new Date(ui.value*1000).toLocaleString());
        }
    });

    this.speedslider = $("#speedSlider");
    this.speedslider.slider({
        value: 500,
        min: 50,
        max: 1000,
        slide: function (event, ui){
            clearInterval(this.runner);
            this.run();
        }.bind(this)
    });

}

Player.prototype.addRoute = function (route) {
    route.points.sort(function (a, b) {
        return new Date(a.dateBegin) - new Date(b.dateBegin);
    });
    route.pointer = 0;

    route.featureGroup = L.featureGroup();
    route.featureGroup.addTo(this.map);
    route.lines = L.polyline([], {color: route.color});
    route.lines.addTo(route.featureGroup);

    if (route.points.length !== 0) {
        var markerPosition = route.points[route.points.length - 1].wgs84Geometry.coordinates;
        route.marker = L.marker([markerPosition[1], markerPosition[0]], {zIndexOffset: 1000});
        route.featureGroup.addLayer(route.marker);
        route.marker.bindPopup(route.individualname + "<br>" +
            new Date(route.points[route.pointer].dateBegin).toLocaleString(), {autoPan: false}).openPopup();
        route.marker.on("move", function (event) {
            route.marker.getPopup().setContent(route.individualname + "<br>" +
                new Date(route.points[route.pointer].dateBegin).toLocaleString());
        });
    }

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
}

Player.prototype.updateMinMax = function(){
    var min= Number.MAX_VALUE;
    var max= 0;

    for (var i = 0; i < this.routes.length; i++){
        if(this.routes[i].points.length  === 0){ // muuta tsekkamaan onko pisteitä aikarajauksen mukaan
            continue;
        }

        min = Math.min(Math.round(new Date(this.routes[i].points[0].dateBegin)/1000), min);
        max = Math.max(Math.round(new Date(this.routes[i].points[this.routes[i].points.length-1].dateBegin)/1000), max);
    }

    this.slider.slider("option", "min", min);
    this.slider.slider("option", "max", max);
    var value = this.slider.slider("option", "value");
    if(value > max || value < min) {
        this.slider.slider("option", "value", this.slider.slider("option", "min"));
    }
    $('#playLabel').html(new Date(this.slider.slider("option", "value")*1000).toLocaleString());
}

Player.prototype.showRoute = function (route) {
    var start = $("#start_time").val();
    var end = $("#end_time").val();

    var points = route.points;
    if (start !== "" || end !== "") {
        points = points_in_timerange(route.points, start, end);
    }

    for (var i = 0, len = points.length; i < len; i++) {
        route.lines.addLatLng([points[i].wgs84Geometry.coordinates[1], points[i].wgs84Geometry.coordinates[0]]);
    }
}

Player.prototype.play = function () {
    if (this.runner) {
        clearInterval(this.runner);
        $("#play").html("&#9658;");
        this.runner = undefined;
    } else {
        $("#play").html("&#9646;&#9646;");
        this.refreshRoutes(true);
        this.drawRoutes();
        this.run();
    }
};

Player.prototype.run = function(){
    var that = this;
    this.runner = setInterval(function() {
        if (that.drawRoutes() === false) {
            clearInterval(this.runner);
        } else {
            var step = Math.round((that.slider.slider("option", "max") - that.slider.slider("option", "min"))/300);
            that.slider.slider("option", "value", that.slider.slider("option", "value") + step);
        }
    }, that.speedslider.slider("option", "max") - that.speedslider.slider("option", "value") + that.speedslider.slider("option", "min"));
}

Player.prototype.drawRoutes = function () {
    var curTime = this.slider.slider("option", "value");

    var animationPlaying = false;

    for (var i = 0, len = this.routes.length; i < len; i++) {
        var route = this.routes[i];
        if (route.points.length <= route.pointer) continue;
        animationPlaying = true;
        var point = route.points[route.pointer];
        while (route.points.length > route.pointer && Math.round(new Date(point.dateBegin))/1000 <= curTime) {
            var coordinates = point.wgs84Geometry.coordinates;
            route.lines.addLatLng([coordinates[1], coordinates[0]]);
            route.marker.setLatLng([coordinates[1], coordinates[0]]);
            route.pointer++;
            point = route.points[route.pointer];
        }
    }

    return animationPlaying;
}

Player.prototype.clearRoute = function (route) {
    route.featureGroup.clearLayers();
    route.lines = L.polyline([], {color: route.color});
    route.lines.addTo(route.featureGroup);
    route.featureGroup.addLayer(route.marker);
    route.marker.openPopup();
}

Player.prototype.refreshRoutes = function (animation) {
    for (var i = 0, len = this.routes.length; i < len; i++) {
        this.clearRoute(this.routes[i]);
        this.routes[i].pointer = 0;
        if(!animation) {
            this.showRoute(this.routes[i]);
        }
    }
}