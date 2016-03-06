$('#table').hide()
errors = []

function init(attachments_of_devices, individual_names, csrf_token) {
    window.attachments_of_devices = attachments_of_devices
    window.individual_names = individual_names
    window.headers = {
        "X-CSRFToken": csrf_token
    }
}


function displayIndividuals(device) {
    $('#table').show()
    $("#attacher").show()
    var rows = '';
    $.each(attachments_of_devices[device], function (index, attachment) {
        var row = '<tr>';
        row += '<td><span id="name' + attachment.individualID + '">' + individual_names[attachment.individualID] + '</span></td>'
        row += '<td>' + $.format.date(attachment.attached, "dd.MM.yyyy HH:mm") + '</td>'

        if (!attachment.removed) {
            $("#attacher").hide();
            row += '<td><input type="text" id="remove_time" name="remove_time" class="dateinput datepicker" placeholder="dd.mm.yyyy HH:mm" onblur="validateDateFormat(this)"></td>'
            var irr = gettext('Irroita');
            row += '<td><a class="btn btn-sm btn-danger" onclick="removeDevice(' + index + ')">' + irr + '</a></td>'
        } else {
            row += '<td>' + $.format.date(attachment.removed, "dd.MM.yyyy HH:mm") + '</td>'
            row += '<td></td>'
        }

        rows += row + '<tr>';
    });
    $('#individuals').html(rows);
    $(".datepicker").datetimepicker();

    if (attachments_of_devices[device].length == 0) {
        $('#individuals').html(
            '<tr><td colspan="4">' + gettext('Ei lintuja') + '</td></tr>');
    }

    showErrors();
}

function attachDevice() {
    var deviceId = $("#selectDevice").val();
    var individualId = $("#individualId").val();
    var timestamp = parseTime($("#start_time").val());

    if (deviceId && validateIndividual(individualId) && validate(timestamp, null, noOverlappingTimeSlices, notInFuture)) {
        $("#attacher").hide();

        $.ajax({
            url: deviceId + "/attach/",
            method: "POST",
            data: {
                individualId: individualId,
                timestamp: timestamp
            },
            headers: headers,
        });

        $.each(attachments_of_devices[deviceId], function (index, attachment) {
            if (!attachment.removed) {
                attachment.removed = timestamp
            }
        })

        attachments_of_devices[deviceId].push({
            individualID: individualId,
            attached: timestamp
        })

        displayIndividuals(deviceId);
    }
    if (errors.length == 0) {
        errors.push(gettext(
            "Kiinnitysajankohdan lisäys onnistui. "))
    }
    showErrors();
}

function removeDevice(index) {
    var deviceId = $("#selectDevice").val();
    var attachment = attachments_of_devices[deviceId][index];
    var individualId = attachment.individualID;
    var attached = attachment.attached;
    var timestamp = parseTime($("#remove_time").val());

    if (deviceId && validateIndividual(individualId) && validate(timestamp, attached, attachedBeforeRemoved, notInFuture)) {
        $("#attacher").show()

        attachment.removed = timestamp;

        $.ajax({
            url: deviceId + "/remove/",
            method: "POST",
            data: {
                individualId: individualId,
                timestamp: timestamp
            },
            headers: headers,
        });

        displayIndividuals(deviceId);
    }
    if (errors.length == 0) {
        errors.push(gettext(
            "Irrotusajankohdan lisäys onnistui. "))
    }
    showErrors();
}

function attachedBeforeRemoved(removed, attached) {
    var a = new Date(pruneTimestring(attached))
    var b = new Date(pruneTimestring(removed))

    if (b.getTime() < a.getTime()) {
        errors.push(gettext("Irroituspäivämäärä ei saa olla ennen kiinnityspäivämäärää. "))
        return false;
    }
    return true;
}

function noOverlappingTimeSlices(timestring) {
    var deviceId = $("#selectDevice").val();
    var time = new Date(pruneTimestring(timestring))

    for (var i = 0; i < attachments_of_devices[deviceId].length; i++) {
        var attachment = attachments_of_devices[deviceId][i];
        if (attachment.removed) {
            var start = new Date(pruneTimestring(attachment.attached))
            var end = new Date(pruneTimestring(attachment.removed))

            if (dateIsBetween(time, start, end)) {
                errors.push(gettext("Kiinnityspäivämäärä ei saa sijoittua sellaiselle ajanjaksolle, jolla laite on jo merkitty kiinnitetyksi. "))
                return false;
            }
        }
    }

    return true;
}

function notInFuture(timestring) {
    time = new Date(pruneTimestring(timestring))

    if (time.getTime() > Date.now()) {
        errors.push(gettext("Päivämäärä ei saa olla tulevaisuudessa. "))
        return false;
    }

    return true;
}

function validate(timestring, attached) {
    valid = true

    if (!validTimestring(timestring)) {
        errors.push(gettext("Päivämäärä ei määritelty! "))
        return false
    }

    for (var i = 2; i < arguments.length; i++) {
        valid &= arguments[i](timestring, attached);
    }

    return valid
}


function validateIndividual(individualID) {
    if (individualID == null) {
        errors.push(gettext("Lintua ei määritelty! "))
        return false
    }
    return true
}

function pruneTimestring(timestring) {
    if (/^[0-9]{4}.[0-9]{2}.[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\+[0-9]{2}:[0-9]{2}:[0-9]{2}$/.test(timestring)) {
        last = timestring.lastIndexOf(":");

        return timestring.slice(0, last);
    }
    return timestring
}

function validTimestring(timestring) {
    if (/^[0-9]{4}.[0-9]{2}.[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\+(?:[0-9][0-9]:)+00$/.test(timestring)) {
        return true
    }
    return false
}

function showErrors() {
    errorMessage = ""
    if (errors.length > 0) {
        for (var i = 0; i < errors.length; i++) {
            errorMessage += errors[i]
        }
    }
    errors = []
    $("#errors").text(errorMessage)
}
