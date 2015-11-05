function DeviceSorter(devices) {

    this.devices = devices;
    this.points = [];

    this.createDeviceSelector(this.devices);

    this.setMap = function (map) {
        this.map = map
    };

    this.currentDevice = 'None'
}

//Sends a request to the rest-controller for documents matching the deviceId.
DeviceSorter.prototype.changeDeviceSelection = function (deviceId) {
    if (deviceId != 'None') {
        messagebox = $("#loading");
        messagebox.text("Tietoja ladataan...");
        lockButtons();
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
    this.currentDevice = deviceId
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
        if (this.points.length === 0) {
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
    $("#save").attr("disabled", false);
};

//Creates a selector for devices.
DeviceSorter.prototype.createDeviceSelector = function (devices) {
    var selector = $("#selectDevice");

    selector.change(function (event) {
        event.preventDefault();
        this.showSaveOrCancelPopup(selector.val())
    }.bind(this));

    selector.addOption = function (option) {
        selector.append("<option value='" + option + "'>" + option + "</option>")
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

    popup = $("#popup");

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