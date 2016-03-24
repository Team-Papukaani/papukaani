var init = function(individuals_data, csrf_token) {
    assert(!!csrf_token);
    window.csrf_token = csrf_token;
    window.individuals_data = individuals_data;

    var sel = $('#selectIndividual');
    makeIndividualSelector(sel, individuals_data);
    window.map = new ChooseMap([]);
    window.currentIndividual = 'None';

    sel.change(function(event) {
        event.preventDefault();

        indId = $('#selectIndividual').val();

        if (!map.hasChanges) {
            changeIndividual(indId);
        } else {
            askSaveCancel(function(err, answer) {
                if (answer === 'save') {
                    savePoints(map, function(err) {
                        if (err) throw err;
                        changeIndividual(indId);
                    });
                } else if (answer === 'no_save') {
                    changeIndividual(indId);
                } else if (answer === 'cancel') {
                    $('#selectIndividual').val(window.currentIndividual);
                }
            });
        }
    });
};

var reset = function() {
    $('#start_time').val('');
    $('#end_time').val('');
    var indId = $('#selectIndividual').val();
    changeIndividual(indId);
};

//Posts publicity data to server. Shows a message and disables the save button while waiting for response.
var savePoints = function(chooseMap, callback) {
    if (!callback) callback = function() {};
    var indId = window.currentIndividual;

    setMessage(gettext('Tallennetaan') + '...');

    lockButtons();
    saveIndividualPoints(indId, chooseMap.points, function(err, data) {
        if (err) {
            setMessage(gettext('Tapahtui virhe!'));
            callback(err);
        }
        assert(data.hasOwnProperty('success'));
        if (data.success) {
            setMessage(gettext('Valmis!'));
            chooseMap.hasChanges = false;
            callback(null);
        } else {
            setMessage(gettext('Tapahtui virhe!'));
            callback(new Error());
        }
        unlockButtons();
    });
};

var askSaveCancel = function(callback) {
    var popup = $('#popup');
    assert(popup.length === 1);

    $("#save_button").click(function(event) {
        callback(null, 'save');
        popup.hide();
    });
    $("#no_save_button").click(function(event) {
        callback(null, 'no_save');
        popup.hide();
    });
    $("#cancel_button").click(function(event) {
        callback(null, 'cancel');
        popup.hide();
    });

    popup.show();
}

var changeIndividual = function(indId, callback) {
    if (!callback) callback = function() {};
    if (indId === 'None') {
        window.map.setPoints([]);
        window.currentIndividual = 'None';
        return callback(null);
    }

    setMessage(gettext('Tietoja ladataaan') + '...');
    lockButtons();

    loadIndividualPoints(indId, function(err, points) {
        if (err) {
            reset();
            setMessage(gettext('Virhe ladattaessa tietoja'));
            return callback(null);
        }
        window.map.setPoints(points);
        clearMessage();
        unlockButtons();
        window.currentIndividual = indId;
        callback(null);
    });
}

var lockButtons = function() {
    $("#selectIndividual").attr("disabled", true);
    $("#save").attr("disabled", true);
    $("#reset").attr("disabled", true);
}

var unlockButtons = function() {
    $("#selectIndividual").attr("disabled", false);
    if (window.map.points.length > 0) {
        $("#save").attr("disabled", false);
    }
    $("#reset").attr("disabled", false);
}

var loadIndividualPoints = function(indId, callback) {
    var url = '../rest/allGatheringsForIndividual?individualId=' + indId;
    $.getJSON(url).done(function(data) {
        assert(isPoints(data));
        callback(null, data);
    }).fail(function() {
        callback(new Error('Error while trying to load points'));
    });
};

var saveIndividualPoints = function(indId, points, callback) {
    assert(isPoints(points));

    $.ajax({
        type: 'POST',
        url: 'changeIndividualGatherings/' + indId + '/',
        data: {
            points: JSON.stringify(points)
        },
        headers: {
            'X-CSRFToken': csrf_token
        }
    }).done(function(data) {
        callback(null, data);
    }).fail(function() {
        callback(new Error());
    });
};

var makeIndividualSelector = function(elem, individuals_data) {
    var sel = $('#selectIndividual');
    assert(sel.length === 1);

    var addOption = function(val, text) {
        // for debugging
        // sel.append("<option value='" + val + "'>" + text + "(" + val + ")" + "</option>") 
        sel.append("<option value='" + val + "'>" + text + "</option>")
    }

    addOption('None', gettext('Valitse lintu'));
    var ids = Object.keys(individuals_data);
    for (var i = 0; i < ids.length; i++) {
        addOption(ids[i], individuals_data[ids[i]]);
    }
};

var setMessage = function(s) {
    $('#message_area').text(s);
}

var clearMessage = function() {
    setMessage('');
};


var assert = function(condition, message) {
    if (!condition) {
        // debugger;
        throw Error("Assert failed" + (typeof message !== "undefined" ? ": " + message : ""));
    }
};

var isPoint = function(x) {
    return (!!x && has(x, 'higherGeography') && has(x, 'temperature'));
};

var isPoints = function(xs) {
    if (!(xs instanceof Array)) return false;
    for (var i = 0; i < xs.length; i++) {
        if (!isPoint(xs[i])) return false;
    }
    return true;
}

var has = function(obj, propName) {
    return obj.hasOwnProperty(propName);
};
