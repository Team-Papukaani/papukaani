function Player(map) {
    this.map = map;
    this.routes = [];
    this.slider = $("#playSlider");
    this.slider.slider({
        range: "min",
        min: 0,
        max: 9007199254740992,
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
        slide:function(event,ui){
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
    var min=9007199254740992;
    var max=0;

    for(var i =0;i<this.routes.length;i++){
        if(this.routes[i].points.length===0){ // muuta tsekkamaan onko pisteitä aikarajauksen mukaan
            continue;
        }

        min = Math.min(Math.round(new Date(this.routes[i].points[0].dateBegin)/1000),min);
        max = Math.max(Math.round(new Date(this.routes[i].points[this.routes[i].points.length-1].dateBegin)/1000),max);
    }
    console.log("min: " + min + " max: " +max);

    this.slider.slider("option","min",min);
    this.slider.slider("option","max",max);
    var value =this.slider.slider("option", "value");
    if(value>max || value<min) {
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

    for (var i in points) {
        route.lines.addLatLng([points[i].wgs84Geometry.coordinates[1], points[i].wgs84Geometry.coordinates[0]]);
    }
}

Player.prototype.play = function(){
    if(this.runner){
        clearInterval(this.runner);
        $("#play").html("&#9658;");
        this.runner=undefined;
    } else {
        $("#play").html("&#9646;&#9646;");
        this.refreshRoutes(true);
        this.drawRoutes();
        this.run();
    }
};

Player.prototype.run = function(){
    var that = this;
    this.runner = setInterval(function(){
        if(that.drawRoutes()===false){
            clearInterval(this.runner);
        } else {
            var step = Math.round((that.slider.slider("option", "max")-that.slider.slider("option", "min"))/300);
            that.slider.slider("option", "value", that.slider.slider("option", "value") + step);
        }
    }, $("#speedSlider").slider("option","max")-$("#speedSlider").slider("option","value")+$("#speedSlider").slider("option","min"));
}

Player.prototype.drawRoutes = function () {
    var curTime = this.slider.slider("option", "value");

    var animationPlaying = false;

    for (var i in this.routes) {
        if(this.routes[i].points.length<=this.routes[i].pointer) continue;
        animationPlaying = true;
        var point = this.routes[i].points[this.routes[i].pointer];
        while(this.routes[i].points.length>this.routes[i].pointer && Math.round(new Date(point.dateBegin))/1000 <= curTime){
            this.routes[i].lines.addLatLng([point.wgs84Geometry.coordinates[1], point.wgs84Geometry.coordinates[0]]);
            this.routes[i].pointer++;
            point = this.routes[i].points[this.routes[i].pointer];
        }
    }

    return animationPlaying;
}

Player.prototype.clearRoute = function (route) {
        route.featureGroup.clearLayers();
        route.lines = L.polyline([], {color: route.color});
        route.lines.addTo(route.featureGroup);
}

Player.prototype.refreshRoutes = function (animation) {
    for (var i in this.routes) {
        this.clearRoute(this.routes[i]);
        this.routes[i].pointer = 0;
        if(!animation) {
            this.showRoute(this.routes[i]);
        }
    }
}





