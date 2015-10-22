function DeviceSorter(documents) {

    this.devices = this.sortIntoDevices(documents);
    this.points = this.getAllPoints(this.devices);

    this.createDeviceSelector(this.devices);

    this.setMap = function (map) {
        this.map = map
    }

}

//Shows the points of a single device. If deviceId not found, all points are shown.
DeviceSorter.prototype.changeDeviceSelection = function (deviceId) {
    if (this.devices[deviceId]) {
        this.points = this.devices[deviceId];
    } else {
        this.points = this.getAllPoints(this.devices);
    }

    this.map.changePoints(this.points)
};

DeviceSorter.prototype.getAllPoints = function (devices) {
    var points = [];
    var device_keys = Object.keys(devices);
    for (i = 0; i < device_keys.length; i++) {
        points = points.concat(devices[device_keys[i]]);
    }
    return points;
}

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

    selector.value = "All";
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

    selector.addOption("All")
    var deviceIds = Object.keys(devices)
    for (var i = 0; i < deviceIds.length; i++) {
        selector.addOption(deviceIds[i])
    }
}