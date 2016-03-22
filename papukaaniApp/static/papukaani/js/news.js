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
        update_news($(this).data("id"));
    });

    $("#createnews").click(function (e) {
        e.preventDefault();
        create_news();
    });

    $("#addnews_tallenna").click(function (e) {
        e.preventDefault();
        create_news_test();
    });

})

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
        title: 'moi',
        language: 'fi',
        content: 'test'
    };
    $.post('/papukaani/news/', postdata, function (data) {
        if (data.status === 'OK') {
            load_news();
        } else {
            alert(data.errors);
        }
    }, 'json');
}

function create_news_test() {
    var postdata = {
        title: $('[name="addnew_title"]').val(),
        language: $('[name="addnew_language"]').children(':selected'),
        content: $('[name="addnew_content"]').val(),
        publishDate: $('[name="publishDate"]').val()
    };
    $.post('/papukaani/news/', postdata, function (data) {
        if (data.status === 'OK') {
            load_news();
        } else {
            alert(data.errors);
        }
    }, 'json');
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
        alert("otsikko: " + n.title);
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