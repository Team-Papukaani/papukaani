function DeviceSorter(devices) {

    this.devices = devices;
    this.points = [];

    this.createDeviceSelector(this.devices);

    this.setMap = function (map) {
        this.map = map
    }

}

//Shows the points of a single device. If deviceId not found, all points are shown.
DeviceSorter.prototype.changeDeviceSelection = function (deviceId) {
    if (deviceId != 'None') {
        console.log("called");
        request = new XMLHttpRequest;
        request.open("GET", "docs/?devId=" + deviceId, true);
        request.onreadystatechange = ready.bind(this);
        request.send(null);
    }
    else {
        console.log("not called");
        this.points = [];
    }
};


function ready() {
    if (request.readyState === 4) {
        console.log(request.responseText);
        this.points = request.responseText;
        this.map.changePoints(this.points);
        console.log("done")
    }
}


DeviceSorter.prototype.getAllPoints = function (devices) {
    var points = [];
    var device_keys = Object.keys(devices);
    for (i = 0; i < device_keys.length; i++) {
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
}

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