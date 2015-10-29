function DeviceSorter(devices) {

    this.devices = devices;
    this.points = [];

    this.createDeviceSelector(this.devices);

    this.setMap = function (map) {
        this.map = map
    }

}

//Sends a request to the rest-controller for documents matching the deviceId.
DeviceSorter.prototype.changeDeviceSelection = function (deviceId) {
    if (deviceId != 'None') {
        messagebox = $("#loading");
        messagebox.text("Tietoja ladataan...");
        button = $("#selectDevice");
        button.attr("disabled", true);
        request = new XMLHttpRequest;
        var path = "../rest/documentsForDevice?devId=" + deviceId + "&format=json";
        request.open("GET", path, true);
        request.onreadystatechange = showPointsForDevice.bind(this);
        request.send(null);
    }
    else {
        this.points = [];
        this.map.changePoints(this.points);
    }
};

//Once the request has a response, changes the sorters points to the ones received in the response.
function showPointsForDevice() {
    if (request.readyState === 4) {
        this.points = [];
        var docs = JSON.parse(request.response);
        for (var i = 0; i < docs.length; i++) {
            this.points.push(docs[i]);
        }
        this.map.changePoints(this.points);
        messagebox = $("#loading");
        messagebox.text("");
        button = $("#selectDevice");
        button.attr("disabled", false);
    }
}

//Resets the option selector to the default value.
DeviceSorter.prototype.resetOption = function () {
    var selector = document.getElementById("selectDevice");

    selector.value = "None";
};

//Creates a selector for devices.
DeviceSorter.prototype.createDeviceSelector = function (devices) {
    var selector = $("#selectDevice");

    selector.change(function (event) {
        event.preventDefault();
        this.changeDeviceSelection(selector.val())
    }.bind(this));

    selector.addOption = function (option) {
        selector.append("<option value='" + option + "'>" + option + "</option>")
    };

    selector.addOption("None");
    for (var i = 0; i < this.devices.length; i++) {
        selector.addOption(this.devices[i])
    }
};