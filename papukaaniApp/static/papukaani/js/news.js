$(function () {
    load_news();

    $("#newslist").on("click", "button.remove", function (e) {
        e.preventDefault();
        if (confirm("Haluatko varmasti poistaa uutisen?")) {
            delete_news($(this).data("id"));
        }
    });

    $("#newslist").on("click", "button.update", function (e) {
        e.preventDefault();
        clear_news_modal();
        $('#news_modal').modal({show: true});
        $('#news_modal h4.modal-title').text("Muokkaa uutista")
        $("#news_tallenna").data("id", $(this).data("id"));
        read_news($(this).data("id"));
    });

    $("#create_news").click(function (e) {
        e.preventDefault();
        clear_news_modal();
        $('#news_modal').modal({show: true});
        $('#news_modal h4.modal-title').text("Lisää uutinen")
        $("#news_tallenna").data("id", "");
    });
    $("#news_tallenna").click(function (e) {
        e.preventDefault();
        $('#messages').text('');
        if ($('#news_title').val() == '') $('#messages').append("Otsikko puuttuu");
        if (tinyMCE.get('news_content').getContent() == "") $('#messages').append("<br>Sisältö puuttuu");
        if ($('#news_language').val() == '') $('#messages').append("<br>Kieli puuttuu");
        if ($('#messages').text()) return;

        if ($(this).data("id")) {
            save_news($(this).data("id"))
        } else {
            save_news();
        }
    });
});

function displayTime(time) {
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
    menubar: false,
    plugins: "image",
    image_description: false,
    toolbar: 'undo redo | bullist numlist | bold italic underline | fontselect fontsizeselect |  image'
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
            if (data.status === 'OK') {
                load_news();
                $('#messages').text("Uutinen luotu onnistuneesti! ");
                clear_news_modal();
            } else {
                alert(data.errors);
            }

        };
    } else {
        //update
        var method = "PUT";
        var url = '/papukaani/news/' + id;
        var callbackfn = function (data) {
            if (data.status === "OK") {
                load_news();
                $('#messages').text("Tiedot tallennettu onnistuneesti!");
                clear_news_modal();
            } else {
                alert(data.errors);
            }
        };
    }
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
    $('#news_language').val('');
    tinyMCE.activeEditor.setContent('');
    $("#news_publishDate").val('');
    sorter.restoreOptions();
}

function delete_news(id) {
    $.ajax({
        url: '/papukaani/news/' + id,
        type: 'DELETE',
        success: function (data) {
            if (data.status === "OK") {
                load_news();
                $('#messages').text("Tiedot poistettu onnistuneesti!");
            } else {
                alert(data.errors);
            }
        },
        dataType: "json"
    });
}

function read_news(id) {
    $.get('/papukaani/news/' + id, function (data) {
        var n = data.news;
        $('#news_title').val(n.title);
        $('#news_language').val(n.language);
        tinyMCE.get('news_content').setContent(n.content);
        $("#news_publishDate").val(n.publishDate ? displayTime(n.publishDate) : '');
        for (var i = 0; i < n.targets.length; i++) {
            $("#selectIndividual").val(n.targets[i]).trigger('change');
        }
    }, "json");
}

function load_news() {
    $.get('/papukaani/news/list', function (data) {
        var list = $("#newslist tbody");
        var html = [];
        $.each(data.news, function (i, v) {
            html.push($('<tr></tr>').append(
                $('<td style="display:none;"></td>').text(v.id)
            ).append(
                $('<td></td>').text(v.title)
            ).append(
                $('<td></td>').text(language(v.language))
            ).append(
                $('<td></td>').text(v.publishDate ? displayTime(v.publishDate) : '')
            ).append(
                $('<td></td>').text(v.targets)
            ).append(
                $('<td><div class="btn-toolbar"><button class="update btn btn-info btn-cons" data-id="' + v.id + '">Muokkaa</button><button class="remove btn btn-danger btn-cons" data-id="' + v.id + '">Poista</button></div></td>')
            ));
        });
        list.html(html)
    }, "json");
}

function language(lang) {
    if (lang == 'fi') return 'Suomi';
    if (lang == 'en') return 'Englanti';
    if (lang == 'sv') return 'Ruotsi';

}

var request = null;

function IndividualSorter(individuals, species) {
    this.birdName = {};
    this.individuals = individuals;
    this.species = species;
    this.createIndividualSelector();
}

IndividualSorter.prototype.restoreOptions = function (individualId) {
    $.each(this.birdName, function (id, name) {
        $('#selectIndividual').showOption(id);
    });
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

    selector.addOption = function (individualId, taxon) {
        var e = '<option value="' + individualId + '">';
        e = e + taxon;
        e = e + '</option>';
        selector.append(e);
        that.birdName[individualId] = taxon;
    };

    $.each(that.species, function (key, s) {
        selector.append('<option value="" disabled>' + s + '</option>');
        $.each(that.individuals[s], function (key, individual) {
            $.each(individual, function (individualId, taxon) {
                selector.addOption(individualId, taxon)
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
