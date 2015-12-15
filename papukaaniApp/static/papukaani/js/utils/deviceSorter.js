function DeviceSorter(devices, restUrl) {

    this.devices = devices;
    this.points = [];
    this.restUrl = restUrl

    this.createDeviceSelector(this.devices);

    this.setMap = function (map) {
        this.map = map
    };

    this.currentDevice = 'None'
}

//Sends a request to the rest-controller for documents matching the deviceId.
DeviceSorter.prototype.changeDeviceSelection = function (deviceId) {
    if (deviceId != 'None') {
        var messagebox = $("#loading");
        messagebox.text("Tietoja ladataan...");
        lockButtons();
        request = new XMLHttpRequest;
        var path = this.requestPath(deviceId);
        request.open("GET", path, true);
        request.onreadystatechange = showPointsForDevice.bind(this);
        request.send(null);
    }
    else {
        this.points = [];
        this.map.changePoints(this.points);
    }
    this.currentDevice = deviceId
};

//Path for all points REST.
DeviceSorter.prototype.requestPath = function (deviceId) {
    return this.restUrl + deviceId + "&format=json";
};

//Extracts a list of points from the documents.
extractPoints = function (documents) {
    var points = [];
    if (documents.length != 0) {
        points = documents[0]["gatherings"];
        for (var p = 1; p < documents.length; p++) {
            points.concat(documents[p]["gatherings"]);
        }
    }
    return points;
};

//Once the request has a response, changes the sorters points to the ones received in the response.
function showPointsForDevice() {
    if (request.readyState === 4) {
        this.points = JSON.parse(request.response);

        this.map.changePoints(this.points);
        var messagebox = $("#loading");
        messagebox.text("");
        if (this.points.length == 0) {
            $("#selectDevice").attr("disabled", false);
            $("#reset").attr("disabled", false);
        }
        else unlockButtons()
    }
}

//Resets the option selector to the default value.
DeviceSorter.prototype.resetOption = function () {
    var selector = document.getElementById("selectDevice");

    selector.value = "None";
    $("#save").attr("disabled", true);
};

//Creates a selector for devices.
DeviceSorter.prototype.createDeviceSelector = function (devices) {
    var selector = $("#selectDevice");

    selector.change(function (event) {
        event.preventDefault();
        this.showSaveOrCancelPopup(selector.val())
    }.bind(this));

    selector.addOption = function (option) {
        val = option.id ? option.id : option
        text = option.nickname ? option.nickname : option

        selector.append("<option value='" + val + "'>" + text+ "</option>")
    };

    selector.addOption("None");
    for (var i = 0; i < this.devices.length; i++) {
        selector.addOption(this.devices[i])
    }
};

//Shows and handles the popup box.
DeviceSorter.prototype.showSaveOrCancelPopup = function (deviceId) {
    if (!this.map.unsaved) {
        this.changeDeviceSelection(deviceId);
        return
    }

    var popup = $("#popup");

    $("#save_button").click(function (event) {
        this.map.send();
        this.changeDeviceSelection(deviceId);
        popup.hide()
    }.bind(this));

    $("#no_save_button").click(function (event) {
        this.changeDeviceSelection(deviceId);
        popup.hide()
    }.bind(this));

    $("#cancel_button").click(function (event) {
        $("#selectDevice").val(this.currentDevice);
        popup.hide()
    }.bind(this));
    popup.show()
};