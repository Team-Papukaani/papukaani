$(function () {
    load_news();

    $("#newslist").on("click", "button.remove", function (e) {
        e.preventDefault();
        if(confirm("Haluatko varmasti poistaa uutisen?")) {
            delete_news($(this).data("id"));
        }
    });

    $("#newslist").on("click", "button.update", function (e) {
        e.preventDefault();
        $('#modify_modal').modal({show: true});
        $("#modify_tallenna" ).attr( "data-id", $(this).data("id"));
        read_news($(this).data("id"));
    });

    $("#addnews_tallenna").click(function (e) {
        e.preventDefault();
        $('#messages').text('');
        if ($('#addnews_title').val()=='') $('#messages').append("Otsikko puuttuu");
        if (tinyMCE.get('addnews_content').getContent()=="") $('#messages').append("<br>Sisältö puuttuu");
        if ($('#addnews_language').val()=='') $('#messages').append("<br>Kieli puuttuu");
        create_news();
    });

    $("#modify_tallenna").click(function (e) {
        e.preventDefault();
        $('#messages').text('');
        if ($('#modify_title').val()=='') $('#messages').append("Otsikko puuttuu");
        if (tinyMCE.get('modify_content').getContent()=="") $('#messages').append("<br>Sisältö puuttuu");
        if ($('#modify_language').val()=='') $('#messages').append("<br>Kieli puuttuu");
        update_news($(this).data("id"));
    });

});

function displayTime(time) {
    var d = new Date(time);
    var day = d.getUTCDate();
    if (day < 10) day = '0'+day;
    var month = d.getUTCMonth() + 1;
    if (month < 10) month = '0'+month;
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
        title: $('#addnews_title').val(),
        language: $('#addnews_language').val(),
        content: tinyMCE.activeEditor.getContent(),
    };
    if($("#addnews_publishDate").val()!="") {
        postdata.publishDate=parseTime($("#addnews_publishDate").val(), "+00:00");
    }
    $.post('/papukaani/news/', postdata, function (data) {
        if (data.status === 'OK') {
            load_news();
            $('#messages').text("Uutinen luotu onnistuneesti! ");
            clear_addnews_modal();
        } else {
            alert(data.errors);
        }
    }, 'json');
}

function clear_addnews_modal() {
    $('#addnews_title').val('');
    $('#addnews_language').val('');
    tinyMCE.activeEditor.setContent('');
    $("#addnews_publishDate").val('');
}

function clear_modifynews_modal() {
    $("#modify_tallenna" ).attr( "data-id", '');
    $('#modify_title').val('');
    $('#modify_language').val('');
    tinyMCE.activeEditor.setContent('');
    $("#modify_publishDate").val('');
}


function update_news(id) {
    var postdata = {
        title: $('#modify_title').val(),
        language: $('#modify_language').val(),
        content: tinyMCE.activeEditor.getContent(),
    };
    if($("#modify_publishDate").val()!="") {
        postdata.publishDate=parseTime($("#modify_publishDate").val(), "+00:00");
    }
    $.ajax({
        url: '/papukaani/news/' + id,
        type: 'PUT',
        data: postdata,
        success: function (data) {
            if (data.status === "OK") {
                load_news();
                $('#messages').text("Tiedot tallennettu onnistuneesti!");
                clear_modifynews_modal();
            } else {
                alert(data.errors);
            }
        },
        dataType: "json"
    });
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
        $('#modify_title').val(n.title);
        $('#modify_language').val(n.language);
        tinyMCE.get('modify_content').setContent(n.content);
        $("#modify_publishDate").val(displayTime(n.publishDate));
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
                $('<td></td>').text(displayTime(v.publishDate))
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
    if(lang=='fi') return 'Suomi';
    if(lang=='en') return 'Englanti';
    if(lang=='sv') return 'Ruotsi';

}