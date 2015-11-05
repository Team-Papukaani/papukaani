function DeviceSorter(devices) {

    this.devices = devices;
    this.documents = [];

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
        this.documents = [];
        this.map.changePoints(extractPoints(this.documents));
    }
    this.currentDevice = deviceId
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
        this.documents = [];
        var docs = JSON.parse(request.response);
        for (var i = 0; i < docs.length; i++) {
            this.documents.push(docs[i]);
        }
        this.map.changePoints(extractPoints(this.documents));
        messagebox = $("#loading");
        messagebox.text("");
        if (this.documents.length == 0) {
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