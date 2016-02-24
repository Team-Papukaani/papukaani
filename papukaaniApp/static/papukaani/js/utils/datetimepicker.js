function datetimestringToUnixtime(string){
    return Math.round(new Date(string) / 1000);
}

function validateDateFormat(element) {
    var format = new RegExp("[0-3][0-9].[0,1][0-9].[0-9]{4} [0-2][0-9]:[0-5][0-9]");
    var val = element.value;
    if (!format.test(val) || val.length != 16) {
        element.value = "";
    }
}

//Parses the given string into an appropriate Date-format.
function parseTime(timestring, offset) {
    var parts = timestring.split(' ');
    var dateparts = parts[0].split('.');

    if(!offset){
        var offset = new Date().getTimezoneOffset()
        offset = ((offset<0? '+':'-')+ // Note the reversed sign!
        pad(parseInt(Math.abs(offset/60)), 2)+ ":" +
        pad(Math.abs(offset%60), 2)) //+ ":00"
    }

    return (dateparts[2] + "-" + dateparts[1] + "-" + dateparts[0] + 'T' + parts[1] + ":00" + offset);
}

function pad(number, length){
    var str = "" + number
    while (str.length < length) {
        str = '0'+str
    }
    return str
}

//Checks if the date is between the two parameters.
function dateIsBetween(date, start, end) {
    return (date.getTime() >= start.getTime() && date.getTime() <= end.getTime());
}

function initDatepicker(){
    $(function () {
            $(".datepicker").datetimepicker();
            $.extend($.datepicker, {
                _checkOffset: function (inst, offset, isFixed) {
                    return offset
                }
            })
        });
}

initDatepicker();



