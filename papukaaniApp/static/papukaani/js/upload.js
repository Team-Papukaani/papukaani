
create_map_with_points = function(data) {
    var points;

    if(data){
        points = JSON.parse(data)
    }

    map = create_map("map", [61.0, 20.0], 5)

    if(points){
        L.polyline(points, {smoothFactor: 25.0}).addTo(map);
    }

}

function displayGpsField () {
    var selectedFormat = $( "#fileFormat" ).val();
    if(fileFormats[selectedFormat] != "") {
        $("#manufacturerIdInputDiv").hide();
        $("#gpsNumber").prop('required',false);
    } else {
        $("#manufacturerIdInputDiv").show();
        $("#gpsNumber").prop('required',true);
    }
}
