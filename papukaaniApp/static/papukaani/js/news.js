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
        $('#news_modal').modal({show: true});
        $('#news_modal h4.modal-title').text("Muokkaa uutista")
        $("#news_tallenna").data("id", $(this).data("id"));
        read_news($(this).data("id"));
    });

    $("#create_news").click(function (e) {
        e.preventDefault();
        $('#news_modal').modal({show: true});
        $('#news_modal h4.modal-title').text("Lisää uutinen")
        $('#news_title').val('');
        $('#news_language').val('');
        tinyMCE.get('news_content').setContent('');
        $("#news_publishDate").val('');
        $("#news_tallenna").data("id","");
    });
    $("#news_tallenna").click(function (e) {
        e.preventDefault();
        $('#messages').text('');
        if ($('#news_title').val() == '') $('#messages').append("Otsikko puuttuu");
        if (tinyMCE.get('news_content').getContent() == "") $('#messages').append("<br>Sisältö puuttuu");
        if ($('#news_language').val() == '') $('#messages').append("<br>Kieli puuttuu");
        if ($('#messages').text()) return;


        if ($(this).data("id")) {
            update_news($(this).data("id"))
        } else {
            create_news();
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

function create_news() {
    var postdata = {
        title: $('#news_title').val(),
        language: $('#news_language').val(),
        content: tinyMCE.activeEditor.getContent(),
    };
    if ($("#news_publishDate").val() != "") {
        postdata.publishDate = parseTime($("#news_publishDate").val(), "+00:00");
    }
    $.post('/papukaani/news/', postdata, function (data) {
        if (data.status === 'OK') {
            load_news();
            $('#messages').text("Uutinen luotu onnistuneesti! ");
            clear_news_modal();
        } else {
            alert(data.errors);
        }
    }, 'json');
}

function update_news(id) {
    var postdata = {
        title: $('#news_title').val(),
        language: $('#news_language').val(),
        content: tinyMCE.activeEditor.getContent(),
    };
    if ($("#news_publishDate").val() != "") {
        postdata.publishDate = parseTime($("#news_publishDate").val(), "+00:00");
    }
    $.ajax({
        url: '/papukaani/news/' + id,
        type: 'PUT',
        data: postdata,
        success: function (data) {
            if (data.status === "OK") {
                load_news();
                $('#messages').text("Tiedot tallennettu onnistuneesti!");
                clear_news_modal();
            } else {
                alert(data.errors);
            }
        },
        dataType: "json"
    });
}

function clear_news_modal() {
    $('.modal').modal('hide');
    $('#news_title').val('');
    $('#news_language').val('');
    tinyMCE.activeEditor.setContent('');
    $("#news_publishDate").val('');
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
    }, "json");
}

function load_news() {
    $.get('/papukaani/news/list', function (data) {
        var list = $("#newslist tbody");
        var html = [];
        $.each(data.news, function (i, v) {
            html.push($('<tr></tr>').append(
                $('<td></td>').text(v.id)
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

function IndividualSorter(restUrl, individuals, species) {
    this.restUrl = restUrl;
    this.birdName = {};
    this.createIndividualSelector(individuals, species);
}
//Sends a request to the rest-controller for documents matching the deviceId.
IndividualSorter.prototype.changeIndividualSelection = function (individualId) {
    request = new XMLHttpRequest;
    var path = this.restUrl + individualId + "&format=json";
    request.open("GET", path, true);
    request.onreadystatechange = addBird.bind(this, individualId);
    request.send(null);
};

IndividualSorter.prototype.removePointsForIndividual = function (individualId) {
    $('#selectIndividual').showOption(individualId);
};

function addBird(ids) {

    if (request.readyState === 4) {

        var data = JSON.parse(request.response);

        for (var i = 0; i < ids.length; i++) {

            if (typeof data[ids[i]] === 'undefined') {
                continue;
            }
            var individualname = data[ids[i]].pop();

            var html = [];
            var id = "individual" + ids[i];
            html.push('<div class="col" data-id="' + ids[i] + '" id="' + id + '">');
            html.push('<button type="button" class="remove" style="float: left; display: block" aria-hidden="true">' +
                '<span class="glyphicon glyphicon-remove" style="float: left" aria-hidden="true"></span></button>' +
                ' <span>' + individualname + '</span> ');

            html.push('</div>');
            $("#birdlist").append(html.join(''));


        }
        request = null;
    }
}
IndividualSorter.prototype.createIndividualSelector = function (individuals, species) {
    var selector = $("#selectIndividual");
    var that = this;

    selector.addOption = function (individualId, taxon) {
        var e = '<option value="' + individualId + '">';
        e = e + taxon;
        e = e + '</option>';
        selector.append(e);
        that.birdName[individualId] = taxon;
    };

    $.each(species, function (key, s) {
        selector.append('<option value="" disabled>' + s + '</option>');
        $.each(individuals[s], function (key, individual) {
            $.each(individual, function (individualId, taxon) {
                selector.addOption(individualId, taxon)
            })
        })
    })

    $("#selectIndividual").change(function () {
        var id = $(this).val();
        if (id === "") return;
        that.changeIndividualSelection([id]);
        $(this).val("");
        $('#selectIndividual').hideOption(id);
    });
};
