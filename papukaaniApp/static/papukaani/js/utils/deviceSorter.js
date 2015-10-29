function DeviceSorter(devices) {

    this.devices = devices;
    this.points = [];

    this.createDeviceSelector(this.devices);

    this.setMap = function (map) {
        this.map = map
    }

}

//Shows the points of a single device. Or none, if no device is specified.
DeviceSorter.prototype.changeDeviceSelection = function (deviceId) {
    if (deviceId != 'None') {
        request = new XMLHttpRequest;
        var path = "../rest/documentsForDevice?devId=" + deviceId + "&format=json";
        request.open("GET", path, true);
        request.onreadystatechange = ready.bind(this);
        request.send(null);
    }
    else {
        this.points = [];
        this.map.changePoints(this.points);
    }
};


function ready() {
    if (request.readyState === 4) {
        this.points = [];
        this.points = JSON.parse(request.response)[0]["gatherings"];
        this.map.changePoints(this.points);
    }
}


DeviceSorter.prototype.getAllPoints = function (devices) {
    var points = [];
    var device_keys = Object.keys(devices);
    for (var i = 0; i < device_keys.length; i++) {
        points = points.concat(devices[device_keys[i]]);
    }
    return points;
};

//Sorts the points in the documents to a dictionary with device ids as keys.
DeviceSorter.prototype.sortIntoDevices = function (documents) {
    var devices = {};
    for (var i = 0; i < documents.length; i++) {
        var deviceId = documents[i].deviceId;
        if (!devices[deviceId]) {
            devices[deviceId] = [];
        }
        for (var j = 0; j < documents[i].gatherings.length; j++) {
            devices[deviceId].push(documents[i].gatherings[j]);
        }
    }

    return devices;
};

//Resets the option selector to the default value.
DeviceSorter.prototype.resetOption = function () {
    var selector = document.getElementById("selectDevice");

    selector.value = "None";
};

//Creates a selector for devices.
DeviceSorter.prototype.createDeviceSelector = function (devices) {
    var selector = $("#selectDevice")

    selector.change(function (event) {
        event.preventDefault()
        this.changeDeviceSelection(selector.val())
    }.bind(this))

    selector.addOption = function (option) {
        selector.append("<option value='" + option + "'>" + option + "</option>")
    }

    selector.addOption("None");
    for (var i = 0; i < this.devices.length; i++) {
        selector.addOption(this.devices[i])
    }
}