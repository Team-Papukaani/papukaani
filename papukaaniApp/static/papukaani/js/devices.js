$('#table').hide()

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
                row += '<td><input type="text" id="remove_time" name="remove_time" class="datepicker" placeholder="dd-mm-yyyy HH:mm"></td>'
                row += '<td><a class="btn btn-sm btn-danger" onclick="removeDevice('+ index +')">Irroita</a></td>'
            } else {
                row += '<td>' + $.format.date(individual.removed, "dd.MM.yyyy HH:mm") + '</td>'
                row += '<td></td>'
            }

            rows += row + '<tr>';
      });

      $('#individuals').html(rows);

      if(devices_and_individuals[device].length == 0) {
            $('#individuals').html('<tr><td colspan="4">Ei lintuja</td></tr>');
      }

}

function attachDevice(){
    var deviceId = $("#selectDevice").val();
    var individualId = $("#individualId").val();
    var timestamp = $("#start_time").val();

    if(deviceId && individualId){
        $("#attacher").hide();

        $.ajax({
            url : deviceId + "/attach/",
            method : "POST",
            data : {
                    individualId : individualId,
                    timestamp : timestamp
                },
            headers : headers
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
}

function removeDevice(index){

    var deviceId = $("#selectDevice").val();
    var individualId = devices_and_individuals[deviceId][index].individualId;
    var timestamp = $("#remove_time").val()

    if(deviceId && individualId){
        $("#attacher").show()

        devices_and_individuals[deviceId][index].removed = timestamp;

        $.ajax({
            url : deviceId + "/remove/",
            method : "POST",
            data : {
                    individualId : individualId,
                    timestamp : timestamp
                },
            headers : headers
        });

        displayIndividuals(deviceId);
    }
}

