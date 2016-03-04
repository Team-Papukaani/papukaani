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

$(function validate() {
        $("#new_individual_form").validate({
            rules: {
                id: {
                    required: true,
                    minlength: 3,
                    maxlength: 20
                },
                taxon: {
                    required: true
                }
            }
        });
        $("#modify_individuals").validate({
             errorPlacement: function(error, element) {
                if (element.attr("name") == "nickname" || element.attr("name") == "taxon" ) {
                    error.insertAfter("#luo");
                } else {
                    error.insertAfter(element);
                }
             },
            rules: {
                id: {
                    required: true,
                    minlength: 3,
                    maxlength: 20
                },
                taxon: {
                    required: true
                },
                ring_id: {
                    number: true
                },
                descriptionUrlEN: {
                    url: true
                },
                descriptionUrlFI: {
                    url: true
                },
                descriptionUrlSV: {
                    url: true
                }
            }
        });
});


$(document).ready(function () {
    runtinymce();
    $('.combobox').combobox();

    $("button.confirmdelete").click(function (e) {
        e.preventDefault();
        confirmdelete($(this).closest('form'));
    });
    validate();
});