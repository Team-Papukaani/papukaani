$(function () {
    load_news();

    var modal_original_data;
    var orginal_content;
    var orginal_bird;
    $('#news_modal').on('shown.bs.modal', function(e) {
        modal_original_data = $( "input, textarea, select" ).serialize();
        orginal_content = tinyMCE.get('news_content').getContent();
        orginal_bird = $("#birdlist").html();
    });

    $("#news_sulje, #news_close_button").click(function (e) {
        // check if the data was changed since the modal was openened
        var modal_new_data = $( "input, textarea, select" ).serialize();
        var new_content = tinyMCE.get('news_content').getContent();
        var new_bird = $("#birdlist").html();
        if( (modal_original_data != modal_new_data) || (orginal_content != new_content) || (orginal_bird != new_bird)) {
            if (!confirm(gettext("Haluatko poistua tallentamatta?"))) {
                e.preventDefault();
            }
            else $('#news_modal').modal('hide');
        }
        else $('#news_modal').modal('hide');
    });

    $("#newslist").on("click", "button.remove", function (e) {
        e.preventDefault();
        if (confirm(gettext("Haluatko varmasti poistaa uutisen?"))) {
            delete_news($(this).data("id"));
        }
    });

    $("#newslist").on("click", "button.update", function (e) {
        e.preventDefault();
        read_news($(this).data("id"));
    });

    $("#create_news").click(function (e) {
        e.preventDefault();
        clear_news_modal();
        $('#news_modal h4.modal-title').text(gettext("Lisää uutinen"))
        $('#news_modal').modal({show: true});
        $("#news_tallenna").data("id", "");
    });
    $("#news_tallenna").click(function (e) {
        e.preventDefault();
        $('#modalmessages').text('');
        if ($('#news_title').val() == '') $('#modalmessages').append("<br>" +  gettext('Otsikko puuttuu'));
        if (tinyMCE.get('news_content').getContent() == "") $('#modalmessages').append("<br>" + gettext('Sisältö puuttuu'));
        if ($('#news_language').val() == '') $('#modalmessages').append("<br> " + gettext('Kieli puuttuu'));
        if ($('#modalmessages').text()) return;

        if ($(this).data("id")) {
            save_news($(this).data("id"))
        } else {
            save_news();
        }
    });
});

function displayTimeWithLeadingZeroes(time) {
    var d = new Date(time);
    var day = d.getUTCDate();
    if (day < 10) day = '0' + day;
    var month = d.getUTCMonth() + 1;
    if (month < 10) month = '0' + month;
    var hours = ('0' + d.getUTCHours()).slice(-2);
    var minutes = ('0' + d.getUTCMinutes()).slice(-2);
    return day + "." + month + "." + d.getFullYear() + " " + hours + ":" + minutes;
}

tinymce.init({
    selector: 'textarea', // change this value according to your HTML
    elementpath: false,
    height: 300,
    resize: false,
    plugins: [
    'advlist autolink lists link image charmap print preview hr anchor pagebreak',
    'searchreplace wordcount visualblocks visualchars code fullscreen',
    'insertdatetime media nonbreaking save table contextmenu directionality',
    'template paste textcolor colorpicker textpattern imagetools'
   ],
   toolbar1: 'insertfile undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | forecolor backcolor | link image print preview',
    image_description: false,
    target_list: false,
    link_title: false
});

function save_news(id) {
    var postdata = {
        title: $('#news_title').val(),
        language: $('#news_language').val(),
        content: tinyMCE.activeEditor.getContent(),
    };
    if ($("#news_publishDate").val() != "") {
        postdata.publishDate = parseTime($("#news_publishDate").val(), "+00:00");
    }

    var targets = [];
    $("#birdlist .col").each(function (i, e) {
        targets.push($(e).data("id"));
    });
    postdata.targets = JSON.stringify(targets);

    if (id === undefined) {
        //create
        var method = "POST";
        var url = '/papukaani/news/';
        var callbackfn = function (data) {
            unlockButtons();
            if (data.status === 'OK') {
                clear_news_modal();
                load_news();
                $('#messages').text(gettext("Uutinen luotu onnistuneesti!"));

            } else {
                alert(data.errors);
            }

        };
    } else {
        //update
        var method = "PUT";
        var url = '/papukaani/news/' + id;
        var callbackfn = function (data) {
            unlockButtons();
            if (data.status === "OK") {
                clear_news_modal();
                load_news();
                $('#messages').text(gettext("Tiedot tallennettu onnistuneesti!"));

            } else {
                alert(data.errors);
            }
        };
    }
    lockButtons();
    $.ajax({
        url: url,
        type: method,
        data: postdata,
        success: callbackfn,
        dataType: "json"
    });
}
function clear_news_modal() {
    $('.modal').modal('hide');
    $("#birdlist").empty();
    $('#news_title').val('');
    $('#modalmessages').empty();
    $('#news_language').val('');
    tinyMCE.activeEditor.setContent('');
    $("#news_publishDate").val('');
    sorter.restoreOptions();
}

function delete_news(id) {
    lockButtons();
    $.ajax({
        url: '/papukaani/news/' + id,
        type: 'DELETE',
        success: function (data) {
            unlockButtons();
            if (data.status === "OK") {
                load_news();
                $('#messages').text(gettext("Tiedot poistettu onnistuneesti!"));
            } else {
                alert(data.errors);
            }
        },
        dataType: "json"
    });
}

function read_news(id) {
    lockButtons();
    $.get('/papukaani/news/' + id, function (data) {
        unlockButtons();
        var n = data.news;
        clear_news_modal();
        $('#news_modal h4.modal-title').text(gettext("Muokkaa uutista"))
        $("#news_tallenna").data("id", id);
        $('#news_title').val(n.title);
        $('#news_language').val(n.language);
        tinyMCE.get('news_content').setContent(n.content);
        $("#news_publishDate").val(n.publishDate ? displayTimeWithLeadingZeroes(n.publishDate) : '');
        for (var i = 0; i < n.targets.length; i++) {
            $("#selectIndividual").val(n.targets[i]).trigger('change');
        }
        $('#news_modal').modal({show: true});
    }, "json");
}

function load_news() {
    showLoadingBar();

    $.get('/papukaani/news/list', function (data) {
        var list = $("#newslist tbody");
        var html = [];
        $.each(data.news, function (i, v) {

            var targets = "";
            $.each(v.targets, function (key, value) {
                targets = targets + (targets ? ', ' : '') + '<b>' + sorter.getName(value) + '</b> ' + sorter.getSpecies(value);
            });

            html.push($('<tr></tr>').append(
                $('<td style="display:none;"></td>').text(v.id)
            ).append(
                $('<td id="title"></td>').text(v.title)
            ).append(
                $('<td id="language"></td>').text(language(v.language))
            ).append(
                $('<td id="publishdate"></td>').text(v.publishDate ? displayTimeWithLeadingZeroes(v.publishDate) : '')
            ).append(
                $('<td id="targets"></td>').html(targets)
            ).append(
                $('<td><div class="btn-toolbar"><button class="update btn btn-info btn-cons" data-id="' + v.id + '"> ' + gettext("Muokkaa") +
                    '</button><button class="remove btn btn-danger btn-cons" data-id="' + v.id + '">' + gettext("Poista") + '</button></div></td>')
            ));
        });
        list.html(html);
        hideLoadingBar();
    }, "json");
}

function language(lang) {
    if (lang == 'fi') return gettext('Suomi');
    if (lang == 'en') return gettext('Englanti');
    if (lang == 'sv') return gettext('Ruotsi');

}

var request = null;

function IndividualSorter(individuals, species) {
    this.birdName = {};
    this.birdSpecies = {};
    this.individuals = individuals;
    this.species = species;

    this.createIndividualSelector();
}

IndividualSorter.prototype.restoreOptions = function (individualId) {
    $.each(this.birdName, function (id, name) {
        $('#selectIndividual').showOption(id);
    });
};

IndividualSorter.prototype.getName = function (individualId) {
    if (!this.birdName.hasOwnProperty(individualId)) return individualId;
    return this.birdName[individualId];
}

IndividualSorter.prototype.getSpecies = function (individualId) {
    if (!this.birdSpecies.hasOwnProperty(individualId)) return "";
    return '(' + this.birdSpecies[individualId] + ')';
}

IndividualSorter.prototype.removePointsForIndividual = function (individualId) {
    $('#selectIndividual').showOption(individualId);
};

function addBird(individualid, name) {
    var html = [];
    var id = "individual" + individualid;
    html.push('<div class="col" data-id="' + individualid + '" id="' + id + '">');
    html.push('<button type="button" class="remove" style="float: left; display: block" aria-hidden="true">' +
        '<span class="glyphicon glyphicon-remove" style="float: left" aria-hidden="true"></span></button>' +
        ' <span>' + name + '</span> ');
    html.push('</div>');
    $("#birdlist").append(html.join(''));
}

IndividualSorter.prototype.createIndividualSelector = function () {
    var selector = $("#selectIndividual");
    var that = this;

    selector.addOption = function (individualId, taxon, species) {
        var e = '<option value="' + individualId + '">';
        e = e + taxon;
        e = e + '</option>';
        selector.append(e);
        that.birdName[individualId] = taxon;
        that.birdSpecies[individualId] = species;
    };

    $.each(that.species, function (key, s) {
        selector.append('<option value="" disabled>' + s + '</option>');
        $.each(that.individuals[s], function (key, individual) {
            $.each(individual, function (individualId, taxon) {
                selector.addOption(individualId, taxon, s)
            });
        });
    });

    $("#selectIndividual").change(function () {
        var id = $(this).val();
        if (id === "") return;
        addBird(id, that.birdName[id]);
        $(this).val("");
        $('#selectIndividual').hideOption(id);
    });
};

function lockButtons() {
    $("#selectIndividual").attr("disabled", true);
    $("button").attr("disabled", true);
}

function unlockButtons() {
    $("#selectIndividual").attr("disabled", false);
    $("button").attr("disabled", false);
}


function showLoadingBar() {
    $(".loadingtext").text(gettext('Uutisia ladataan') + '...');
    $('#loading').modal({
        backdrop: 'static',
        keyboard: false
    });
}
function hideLoadingBar() {
    $('#loading').modal('hide');
}

$(document).on('focusin', function(e) {
        if ($(e.target).closest(".mce-window").length) {
            e.stopImmediatePropagation();
        }
});