function create_map(container, latlong, zoom) {
    var map = new L.map(container, {zoomControl: false, maxZoom: 15});
    var layers = {
        mm: L.tileLayer('http://tiles.kartat.kapsi.fi/peruskartta/{z}/{x}/{y}.jpg', {
            attribution: 'Maanmittauslaitos'
        }),
        osm: L.tileLayer('http://otile1.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        }),
        otm: L.tileLayer('http://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
            maxZoom: 16,
            attribution: 'Map data: &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'
        }),
        satellite: L.tileLayer('http://oatile1.mqcdn.com//tiles/1.0.0/sat/{z}/{x}/{y}.jpg', {
            attribution: 'MapQuest Aerial'
        }),
        geobiologicalProvinces: L.tileLayer.wms("http://maps.luomus.fi/geoserver/ows", {
            layers: 'test:eliomaakunnat',
            format: 'image/png',
            transparent: true,
            version: '1.3.0'
        })
    };

    var baseMaps = {
        gettext("Maailmankartta"): layers.osm,
        gettext("Topografia"): layers.otm,
        gettext("Maanmittauslaitos"): layers.mm),
        gettext("Satelliitti"): layers.satellite
    };

    var overlays = {
        gettext("Eliömaakunnat"): layers.geobiologicalProvinces
    };

    layers.osm.addTo(map);
    L.control.layers(baseMaps, overlays).addTo(map);

    map.setView(latlong, zoom);
    L.control.zoom({position: 'topright'}).addTo(map);

    L.control.scale().addTo(map);

    return map;
}
