function confirm (form) {

    var popup = $("#delete_confirm_popup");

    $("#yes_button").click(function (event) {
        var deleteField = document.createElement("input");
        deleteField.type = "hidden";
        deleteField.name = "delete";
        deleteField.value = "1";
        form.appendChild(deleteField)
        form.submit()
    });

    $("#cancel_button").click(function (event) {
        popup.hide()
    });
    popup.show()
};

$(document).ready(function(){
    $('.combobox').combobox();
});