var DEBUG = false;

Promise.onPossiblyUnhandledRejection(function(error){
    if (DEBUG) debugger;
    throw error;
});

// globals object 
var devs = {};

var init = function(devices, individuals, csrf_token) {

    assert(forAll(devices, isDevice));
    assert(forAll(individuals, isIndividual));
    assert(!!csrf_token);

    devs.allDevices = devices;
    devs.individuals = individuals;
    devs.loaded = {
        deviceID: null,
        atts: []
    };
    devs.headers = {
        "X-CSRFToken": csrf_token
    };

    devs.templates = {};
    devs.templates.attDisplay = _.template($('#att-display-template').html());
    devs.templates.attEditing = _.template($('#att-editing-template').html());
    devs.templates.attsList = _.template($('#device-atts-template').html());
    devs.templates.noneNote = _.template($('#none-note-template').html());
    devs.templates.loadingError = _.template($('#loading-error-template').html());

    var selectDevice = $('#selectDevice');
    selectDevice.on('change', function (e) {
        var deviceID = selectDevice.val();
        changeDevice(deviceID).done();
    });
};

var renderDisplayedAtt = function(att) {
    
    var el = $(devs.templates.attDisplay({
        att: att,
        individualName: getByID(
            devs.individuals, att.individualID).nickname
    }));

    el.find('.edit-button').on('click', function (e) {
        startEditingAtt(att.id);
    });
    el.find('.delete-button').on('click', function (e) {
        tryDeleteAtt(att.id).done();
    });

    return el;
};

var renderEditingAtt = function(att) {
    return _renderEditingNewOrExistingAtt(att);
};

var renderEditingNewAtt = function() {
    return _renderEditingNewOrExistingAtt(null);
}

var _renderEditingNewOrExistingAtt = function (arg) {
    var isNew;
    var att;

    if (arg === null) {
        isNew = true;
        att = {};
    } else {
        isNew = false;
        att = arg;
    }

    var el = $(devs.templates.attEditing({
        isNew: isNew,
        att: att,
        individuals: devs.individuals
    }));

    el.find('.cancel-button').on('click', function (e) {
        cancelEditingAtt(el);
    });

    el.find('.save-button').on('click', function (e) {
        trySaveEditedAtt(el).done();
    });

    el.find('.datepicker').datetimepicker();

    return el;
};

var renderAttsList = function(atts) {
    assert(forAll(atts, isAttachment));

    var el = $(devs.templates.attsList({
        deviceID: devs.loaded.deviceID
    }));

    if (atts.length > 0) {
        _.each(atts, function (att) {
            var attEl = renderDisplayedAtt(att);
            el.find('tbody').append(attEl);
        });
    } else {
        addNoneNote(el);
    }

    return el;
};

var renderDeviceView = function(atts) {
    var frag = $(document.createDocumentFragment());

    frag.append(renderAttsList(atts));

    var newButton = $('<a class="btn btn-md btn-primary">')
            .addClass('new-button')
            .addClass('pull-right')
            .text(gettext('Uusi kiinnitys'));
    newButton.on('click', function (e) {
        startEditingNewAtt();
    });
    frag.append(newButton);

    return frag;
};

////////////////////////////////////////////////////////////////

var startEditingAtt = function(attID) {
    var el = $('#att-' + attID);

    var att = getByID(devs.loaded.atts, attID);
    var newEl = renderEditingAtt(att);
    el.replaceWith(newEl);
    disableButtons();
    $('#selectDevice').attr('disabled', true);
};

var startEditingNewAtt = function() {
    removeNoneNote($('.atts-list'));

    var newEl = renderEditingNewAtt();
    $('.atts-list tbody').append(newEl);
    disableButtons();
    $('#selectDevice').attr('disabled', true);
}

var disableButtons = function() {
    $('.new-button').addClass('disabled');  
    $('.edit-button, .delete-button').addClass('disabled');
}

var enableButtons = function() {
    $('.new-button').removeClass('disabled');
    $('.edit-button, .delete-button').removeClass('disabled');
}

var addNoneNote = function(el) {
    var noneNote = devs.templates.noneNote();
    el.find('tbody').append(noneNote);
    return el;
}

var removeNoneNote = function(el) {
    el.find('tbody .none-note').remove();
    return el;
}

var cancelEditingAtt = function(el) {

    $('#devs-main').empty().append(renderDeviceView(devs.loaded.atts));
    clearMessage();
    enableButtons();
    $('#selectDevice').attr('disabled', false);
};

// create if new, update if existing
var trySaveEditedAtt = function(el) {

    var newData = getEditedAttData(el);

    try {
        validateAtt(newData, devs.loaded.atts);
    } catch (err) {
        if (err instanceof ValidationError) {
            setErrorMessage(err.message);
            return Promise.resolve();
        } else {
            return Promise.reject(err);
        }
    }

    var wasNew = isNewAtt(devs.loaded.atts, newData);

    return Promise.resolve().then(function () {
        setInfoMessage(gettext('Tallennetaan') + '...');            
        return saveAtt(devs.loaded.atts, newData);
    }).then(function (att) {
        // resort and rerender 
        if (wasNew) {
            devs.loaded.atts.push(att);
        } else {
            replaceByID(devs.loaded.atts, att.id, att);
        }
        sortAtts(devs.loaded.atts);
        $('#devs-main').empty().append(renderDeviceView(devs.loaded.atts));
        clearMessage();
        enableButtons();
        $('#selectDevice').attr('disabled', false);
    }).catch(reportErrors(gettext('Virhe kun yritettiin tallentaa')));
};

var tryDeleteAtt = function(attID) {

    disableButtons();
    setInfoMessage(gettext('Poistetaan') + '...');

    return deleteAtt(attID).then(function () {
        devs.loaded.atts = deleteByID(devs.loaded.atts, attID);
        
        var el = $('#att-' + attID);

        el.remove();
        enableButtons();
        clearMessage();
    }).catch(reportErrors(gettext('Virhe kun yritettiin poistaa')));
}

var changeDevice = function(deviceID) {

    var loadingStub = renderAttsList([]);
    var newDeviceID = $('#selectDevice').val();

    return Promise.resolve().then(function() {
        $('#devs-main .atts-list').replaceWith(loadingStub);
        setInfoMessage(gettext('Ladataan') + '...');
        $('#selectDevice').attr('disabled', true);
        return getAtts(deviceID);
    }).then(function (atts) {
        sortAtts(atts);
        devs.loaded = {
            deviceID: newDeviceID,
            atts: atts
        };
        $('#devs-main').empty().append(renderDeviceView(atts));
        clearMessage();
        $('#selectDevice').attr('disabled', false);
    }).catch(function (err) {
        $('#devs-main').empty().append(devs.templates.loadingError());
        reportErrors(gettext('Virhe ladattaessa tietoja'))(err);
        $('#selectDevice').attr('disabled', false);
    });
};

var getEditedAttData = function(el) {

    var data = {};
    data.deviceID = devs.loaded.deviceID;
    data.individualID = el.find('.select-individual').val();
    data.attached = parseTime(el.find('[name=attach-time]').val());

    var s = el.find('[name=remove-time]').val().trim();
    if (s.length > 0) {
        data.removed = parseTime(s);
    }

    var isNew = el.hasClass('new');
    if (isNew) {
        data.id = null;
    } else {
        data.id = el.attr('data-id');
    }

    return data;
};


////////////////////////////////////////////////////////////////


var saveAtt = function(oldAtts, att) {

    var isNew = isNewAtt(oldAtts, att);
    var method = isNew ? 'POST' : 'PUT';
    var url = isNew ? 'attachments/' : 'attachments/' + att.id;

    dlog('-- @ saveAtt w/', isNew, att, 'ready to ', method, url);

    return Promise.resolve($.ajax({
        url: url,
        method: method,
        data: att,
        headers: devs.headers
    })).catch(normalizeJQueryError)
    .then(getDataOrFailure);
}

var deleteAtt = function(attID) {
    return Promise.resolve($.ajax({
        url: 'attachments/' + attID,
        method: 'DELETE',
        headers: devs.headers
    })).catch(normalizeJQueryError)
    .then(getDataOrFailure);
}

// ascending order based on attach time
var sortAtts = function (atts) {
    var cmp = function (a1, a2) {
        t1 = totime(a1.attached);
        t2 = totime(a2.attached);
        if (t1 === t2) return 0;
        if (t1 < t2) return -1;
        return 1;
    }
    atts.sort(cmp);
}

var getAtts = function(deviceID) {

    return Promise.resolve($.ajax({
        url: 'attachments?deviceID=' + deviceID,
        method: 'GET'
    })).catch(normalizeJQueryError)
    .then(getDataOrFailure);
}

var normalizeJQueryError = function(thrown) {
    if (isJqXHR(thrown)) {
        throw new JQueryRequestError('', thrown);
    } else {
        throw thrown;
    }
}

var getDataOrFailure = function(data) {
    if (data.status === 'OK') {
        return data.data;
    } else if (data.status === 'REFUSE') {
        throw new RefuseFromServer('', data);
    } else {
        throw new ErrorFromServer('', data);
    }
};

var reportErrors = function(prefix) {
    return function (err) {
        if (err instanceof RefuseFromServer && err.data.message) {
            setErrorMessage(prefix + ': ' + err.data.message);
            // don't throw
        } else {
            setErrorMessage(prefix + ': ' + err.name + ': ' +  err.message);
            throw err;
        }
    };
};


////////////////////////////////////////////////////////////////


var validateAtt = function(att, oldAtts) {

    if (att.individualID === null) {
        throw new ValidationError(gettext('Lintua ei määritelty!'));
    }

    if (!validTimestamp(att.attached)) {
        throw new ValidationError(gettext('Kiinnityspäivämäärää ei määritelty!'));
    }

    if (att.removed && (totime(att.removed) < totime(att.attached))) {
        throw new ValidationError(gettext('Irroitus ei saa olla ennen kiinnitystä!'));
    }

    var now = (new Date()).getTime();
    if (now < (totime(att.attached)) || (att.removed && now < totime(att.removed))) {
        throw new ValidationError(gettext('Päivämäärä ei saa olla tulevaisuudessa!'));
    }

    var overlapping = overlapsWithOld(att, oldAtts);
    if (overlapping !== null) {
        var name = getByID(devs.individuals, overlapping.individualID).nickname;
        throw new ValidationError(gettext('Laite on tuona aikana jo kiinni linnussa.') + name);
    }
}

var isNewAtt = function(oldAtts, newAtt) {
    if (!newAtt.id) return true;
    assert(getByID(oldAtts, newAtt.id) !== null) 
    return false;
}
function validTimestamp(timestamp) {
    if (/^[0-9]{4}.[0-9]{2}.[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\+(?:[0-9][0-9]:)+00$/.test(timestamp)) {
        return true
    }
    return false
}

// convert lajistore timestamp to milliseconds since epoch
var totime = function(timestamp) {
    assert(validTimestamp(timestamp));

    var t = (new Date(pruneTimestamp(timestamp))).getTime();
    return t;
};

function pruneTimestamp(timestamp) {
    if (/^[0-9]{4}.[0-9]{2}.[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\+[0-9]{2}:[0-9]{2}:[0-9]{2}$/.test(timestamp)) {
        last = timestamp.lastIndexOf(":");
        return timestamp.slice(0, last);
    }
    return timestamp
}

var rangesOverlap = function (range1, range2) {
    assert(range1[0] <= range1[1] && range2[0] <= range2[1]);

    var earlier, later;

    if (range1[0] <= range2[0]) {
        earlier = range1;
        later = range2;
    } else {
        earlier = range2;
        later = range1;
    }

    return (later[0] < earlier[1]);
};

var overlapsWithOld = function (att, oldAtts) {

    var now = (new Date()).getTime();
    var start1 = totime(att.attached);
    var end1 = att.removed ? totime(att.removed) : now;

    for (var i = 0; i < oldAtts.length; i++) {
        if (oldAtts[i].id === att.id) continue;
        var start2 = totime(oldAtts[i].attached);
        var end2 = oldAtts[i].removed ? totime(oldAtts[i].removed) : now;
        if (rangesOverlap([start1, end1], [start2, end2])) return oldAtts[i];
    }
    return null;
}


////////////////////////////////////////////////////////////////


var getByID = function(xs, id) {
    for (var i = 0; i < xs.length; i++) {
        if (xs[i].id === id) return xs[i];
    }
    return null;
}

var deleteByID = function(xs, id) {
    return _.filter(xs, function(x) {
        if (x.id === id) return false;
        return true;
    });
}

var replaceByID = function(xs, id, x) {
    for (var i = 0; i < xs.length; i++) {
        if (xs[i].id === id) xs[i] = x;
    }
}


////////////////////////////////////////////////////////////////

var setErrorMessage = function(s) {
    _setMessage({
        text: s,
        type: "error"
    });
}

var setInfoMessage = function(s) {
    _setMessage({
        text: s,
        type: "info"
    });
};

var _setMessage = function(opts) {
    var el = $('#message_area');
    el.text(opts.text);
    el.removeClass('text-info text-danger');
    el.removeClass('error-message info-message');
    if (opts.type === 'info') {
        el.addClass('text-info info-message');
    } else if (opts.type === 'error') {
        el.addClass('text-danger error-message');
    }
};

var clearMessage = function() {
    setInfoMessage("");
};


////////////////////////////////////////////////////////////////


var mkCustomError = function(name, init) {

    var CustomError = function(message) {
        var error = Error.call(this, message);
        this.name = name;
        this.message = error.message;
        this.stack = error.stack;
        if (typeof init === 'function') {
            init.apply(this, arguments);
        }
    }

    CustomError.prototype = Object.create(Error.prototype);
    CustomError.prototype.constructor = CustomError;

    return CustomError;
}

var ValidationError = mkCustomError('ValidationError');

var RefuseFromServer = mkCustomError('RefuseFromServer', function(message, data) {
    this.data = data;
});

var ErrorFromServer = mkCustomError('ErrorFromServer', function(message, data) {
    this.data = data;
});

var JQueryRequestError = mkCustomError('JQueryRequestError', function(message, data) {
    this.data = data;
});


////////////////////////////////////////////////////////////////


var assert = function(condition, message) {
    if (!condition) {
        if (DEBUG) debugger;
        throw Error("Assert failed" + (typeof message !== "undefined" ? ": " + message : ""));
    }
};

var isIndividual = function(x) {
    return hasProperties(x, ['nickname']);
}

var isDevice = function(x) {
    return hasProperties(x, ['deviceType', 'deviceManufacturerID']);
}

var isAttachment = function(x) {
    return hasProperties(x, ['individualID', 'deviceID', 'attached']);
}

var isJqXHR = function(x) {
    return hasProperties(x, ['readyState', 'statusText']);
}

var forAll = function(xs, f) {
    assert(xs instanceof Array);
    for (var i = 0; i < xs.length; i++) {
        if (!f(xs[i])) return false;
    }
    return true;
}

var hasProperties = function(x, props) {
    assert(props instanceof Array);
    for (var i = 0; i < props.length; i++) {
        if (!x.hasOwnProperty(props[i])) return false;
    }
    return true;
}

var dlog = function() {
    if (DEBUG) {
        console.log.apply(console, arguments);
    }
};

////////////////////////////////////////////////////////////////

