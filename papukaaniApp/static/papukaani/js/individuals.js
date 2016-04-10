function confirmdelete(form) {

    var popup = $("#delete_confirm_popup");

    $("#yes_button").click(function (event) {
        $('<input>').attr({
            type: 'hidden',
            name: 'delete',
            value: 1
        }).appendTo(form);
        form.submit();
    });

    $("#cancel_button").click(function (event) {
        popup.hide()
    });
    popup.show()
};

tinymce.init({
    selector: 'textarea', // change this value according to your HTML
    elementpath: false,
    height: 300,
    resize: false,
    menubar: false
});

$('form').each(function () { // attach to all form elements on page
    $.validator.setDefaults({
        ignore: []
    });
    var validator = $(this).validate({
        rules: {
            nickname: {
                required: true,
                minlength: 2,
            },
            taxon: {
                required: true
            },
            ring_id: {},
            descriptionUrlEN: {
                url: true
            },
            descriptionUrlFI: {
                url: true
            },
            descriptionUrlSV: {
                url: true
            }
        },
        showErrors: function (errorMap, errorList) {

            $.each(this.successList, function (index, value) {
                $(value).popover('hide');
            });


            $.each(errorList, function (index, value) {

                console.log(value.message);

                var _popover = $(value.element).popover({
                    trigger: 'manual',
                    placement: 'top',
                    content: value.message,
                    template: '<div class="popover"><div class="arrow"></div><div class="popover-inner"><div class="popover-content"><p></p></div></div></div>'
                });

                _popover.data('bs.popover').options.content = value.message;

                $(value.element).popover('show');
            });
        }
    });
});

$(document).ready(function () {
    $('.combobox').combobox();
    $("button.confirmdelete").click(function (e) {
        e.preventDefault();
        confirmdelete($(this).closest('form'));
    });
    jQuery.extend(jQuery.validator.messages, { //käännettävä teksti
        required: gettext("Tämä kenttä on pakollinen."),
        minlength: jQuery.validator.format(gettext("Nimen pitää olla vähintään {0} kirjaimen pituinen.")),
        url: jQuery.validator.format(gettext("Anna oikea http(s) osoite"))
    });
});