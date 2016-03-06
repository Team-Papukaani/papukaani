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
                minlength: 3,
                maxlength: 20
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
        required: "Tämä kenttä on pakollinen",
        remote: "Please fix this field.",
        email: "Please enter a valid email address.",
        url: "Please enter a valid URL.",
        date: "Please enter a valid date.",
        dateISO: "Please enter a valid date (ISO).",
        number: "Please enter a valid number.",
        digits: "Please enter only digits.",
        creditcard: "Please enter a valid credit card number.",
        equalTo: "Please enter the same value again.",
        accept: "Please enter a value with a valid extension.",
        maxlength: jQuery.validator.format("Please enter no more than {0} characters."),
        minlength: jQuery.validator.format("Please enter at least {0} characters."),
        rangelength: jQuery.validator.format("Please enter a value between {0} and {1} characters long."),
        range: jQuery.validator.format("Please enter a value between {0} and {1}."),
        max: jQuery.validator.format("Please enter a value less than or equal to {0}."),
        min: jQuery.validator.format("Please enter a value greater than or equal to {0}.")
    });
});