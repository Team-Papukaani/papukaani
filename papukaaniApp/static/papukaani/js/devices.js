$('#table').hide()
errors = []

function init(devices, indivs, csrf_token){
    devices_and_individuals = devices
    individuals = indivs

    headers = {
               "X-CSRFToken" :  csrf_token
              }
}



function displayIndividuals(device) {
      $('#table').show()
      $("#attacher").show()
      var rows = '';
      $.each(devices_and_individuals[device], function(index, individual) {
            var row = '<tr>';
            row += '<td><span id="name' + individual.individualId + '">' + individuals[individual.individualId] + '</span></td>'
            row += '<td>' + $.format.date(individual.attached, "dd.MM.yyyy HH:mm") + '</td>'

            if(!individual.removed) {
                $("#attacher").hide();
                row += '<td><input type="text" id="remove_time" name="remove_time" class="dateinput datepicker" placeholder="dd.mm.yyyy HH:mm" onblur="validateDateFormat(this)"></td>'
                row += '<td><a class="btn btn-sm btn-danger" onclick="removeDevice('+ index +')">Irroita</a></td>'
            } else {
                row += '<td>' + $.format.date(individual.removed, "dd.MM.yyyy HH:mm") + '</td>'
                row += '<td></td>'
            }

            rows += row + '<tr>';
      });
      $('#individuals').html(rows);
      $(".datepicker").datetimepicker();

      if(devices_and_individuals[device].length == 0) {
            $('#individuals').html('<tr><td colspan="4">Ei lintuja</td></tr>');
      }

      showErrors()

}

function attachDevice(){
    var deviceId = $("#selectDevice").val();
    var individualId = $("#individualId").val();
    var timestamp = parseTime($("#start_time").val());

    if(deviceId && validateIndividual(individualId) && validate(timestamp, null, noOverlappingTimeSlices, notInFuture)){
        $("#attacher").hide();

        $.ajax({
            url : deviceId + "/attach/",
            method : "POST",
            data : {
                    individualId : individualId,
                    timestamp : timestamp
                },
            headers : headers,
        });

        $.each(devices_and_individuals[deviceId], function(index, individual){
            if(!individual.removed){
                individual.removed = timestamp
            }
        })

        devices_and_individuals[deviceId].push({
            individualId : individualId,
            attached : timestamp
        })

        displayIndividuals(deviceId);
    }
    if(errors.length == 0){
        errors.push("Kiinnitysajankohdan lisäys onnistui. ")
    }
    showErrors()
}

function removeDevice(index){

    var deviceId = $("#selectDevice").val();
    var individualId = devices_and_individuals[deviceId][index].individualId;
    var attached = devices_and_individuals[deviceId][index].attached;
    var timestamp = parseTime($("#remove_time").val());

    if(deviceId && validateIndividual(individualId) && validate(timestamp, attached, attachedBeforeRemoved, notInFuture)){
        $("#attacher").show()

        devices_and_individuals[deviceId][index].removed = timestamp;

        $.ajax({
            url : deviceId + "/remove/",
            method : "POST",
            data : {
                    individualId : individualId,
                    timestamp : timestamp
                },
            headers : headers,
        });

        displayIndividuals(deviceId);
    }
    if(errors.length == 0){
        errors.push("Irrotusajankohdan lisäys onnistui. ")
    }
    showErrors()
}

function attachedBeforeRemoved(removed, attached){
    var a = new Date(pruneTimestring(attached))
    var b = new Date(pruneTimestring(removed))

    if(b.getTime() < a.getTime()){
        errors.push("Irroituspäivämäärä ei saa olla ennen kiinnityspäivämäärää. ")
        return false;
    }
    return true;
}

function noOverlappingTimeSlices(timestring){
    var deviceId = $("#selectDevice").val();
    var time = new Date(pruneTimestring(timestring))
    var valid = true

    $.each(devices_and_individuals[deviceId], function(index, individual){
        if(individual.removed){
            var start = new Date(pruneTimestring(individual.attached))
            var end = new Date(pruneTimestring(individual.removed))

            if(dateIsBetween(time, start, end)){
                errors.push("Kiinnityspäivämäärä ei saa sijoittua sellaiselle ajanjaksolle, jolla laite on jo merkitty kiinnitetyksi. ")
                valid = false;
            }
        }
    })

    return valid;
}

function notInFuture(timestring){
    time = new Date(pruneTimestring(timestring))

    if(time.getTime() > Date.now()){
        errors.push("Päivämäärä ei saa olla tulevaisuudessa. ")
        return false;
    }

    return true;
}

function validate(timestring, attached){
    valid = true

    if(!validTimestring(timestring)){
        errors.push("Päivämäärä ei määritelty! ")
        return false
    }

    for(var i = 2; i < arguments.length; i++){
        valid &= arguments[i](timestring, attached);
    }

    return valid
}

function validateIndividual(individualId){
    if(individualId == null){
        errors.push("Lintua ei määritelty! ")
        return false
    }
    return true
}

function pruneTimestring(timestring){
    if(/^[0-9]{4}.[0-9]{2}.[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\+[0-9]{2}:[0-9]{2}:[0-9]{2}$/.test(timestring)){
        last = timestring.lastIndexOf(":");

        return timestring.slice(0, last);
    }
    return timestring
}

function validTimestring(timestring){
    if(/^[0-9]{4}.[0-9]{2}.[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\+(?:[0-9][0-9]:)+00$/.test(timestring)){
        return true
    }
    return false
}

function showErrors(){
    errorMessage = ""
    if(errors.length > 0){
        for(var i = 0; i < errors.length; i++){
            errorMessage += errors[i]
        }
    }
    errors = []
    $("#errors").text(errorMessage)
}