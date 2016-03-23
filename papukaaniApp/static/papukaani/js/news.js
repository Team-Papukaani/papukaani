$(function () {
    load_news();

    $("#newslist").on("click", "button.remove", function (e) {
        e.preventDefault();
        delete_news($(this).data("id"));
    });
    $("#newslist").on("click", "button.read", function (e) {
        e.preventDefault();
        read_news($(this).data("id"));
    });
    $("#newslist").on("click", "button.update", function (e) {
        e.preventDefault();
        read_news($(this).data("id"));
        $('#modify_modal').modal({show: true});
        //update_news($(this).data("id"));
    });

    $("#addnews_tallenna").click(function (e) {
        e.preventDefault();
        create_news();
    });

});

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
        publishDate: parseTime($("#addnews_publishDate").val(), "+00:00")
        //language: $('[name="addnew_language"]').children(':selected'),
        //content: $('[name="addnew_content"]').val(),
        //publishDate: $('[name="publishDate"]').val()
    };
    $.post('/papukaani/news/', postdata, function (data) {
        if (data.status === 'OK') {
            load_news();
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
    $('#modify_title').val('');
    $('#modify_language').val('');
    tinyMCE.activeEditor.setContent('');
    $("#modify_publishDate").val('');
}


function update_news(id) {
    var postdata = {
        title: 'updated',
        language: 'sv',
        content: 'päivitetty uutinen',
        targets: [1234, 1234]
    };
    $.ajax({
        url: '/papukaani/news/' + id,
        type: 'PUT',
        data: postdata,
        success: function (data) {
            if (data.status === "OK") {
                load_news();
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
        tinyMCE.activeEditor.setContent(n.content);
        $("#modify_publishDate").val(n.publishDate);
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
                $('<td></td>').text(v.language)
            ).append(
                $('<td></td>').text(v.publishDate)
            ).append(
                $('<td></td>').text(v.targets)
            ).append(
                $('<td><button class="remove" data-id="' + v.id + '">Poista</button></td>')
            ).append(
                $('<td><button class="read" data-id="' + v.id + '">Avaa</button></td>')
            ).append(
                $('<td><button class="update" data-id="' + v.id + '">Muokkaa</button></td>')
            ));
        });
        list.html(html)
    }, "json");
}