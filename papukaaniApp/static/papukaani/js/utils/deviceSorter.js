function DeviceSorter() {

    this.documents = [];

    this.setDevices = function (devices) {
        this.createDeviceSelector(devices);
        this.type = "Device"
    };

    this.setIndividuals = function (individuals) {
        this.createIndividualSelector(individuals);
        this.type = "Individual"
    };

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
        var path = "../rest/documentsFor" + this.type + "?devId=" + deviceId + "&format=json";
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
        var messagebox = $("#loading");
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
    for (var i = 0; i < devices.length; i++) {
        selector.addOption(devices[i])
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

/* Individual spesifics */

//Creates a selector for individuals (individualId:taxon).
DeviceSorter.prototype.createIndividualSelector = function (individuals) {
    var selector = $("#selectDevice");

    selector.change(function (event) {
        event.preventDefault();
        this.showSaveOrCancelPopup(selector.val())
    }.bind(this));

    selector.addOption = function (individualId, taxon) {
        selector.append("<option value='" + individualId + "'>" + taxon + "</option>")
    };

    selector.addOption("None","Valitse");
    $.each(individuals, function(species, individualsOfSpecies){
        selector.append("<option disabled='disabled'>" + species + "</option>")
        $.each(individualsOfSpecies, function(key, individual){
            $.each(individual, function(individualId, taxon){
                selector.addOption(individualId, taxon)
            })
        })
    })
};