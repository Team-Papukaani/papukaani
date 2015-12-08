function showPopup(message, redirect_url) {

    var popup = $("#popup");
    $("#popup_message").html(message);

    function yes_event(){
        window.location.replace(redirect_url);
    }

    function cancel_event(){
        popup.hide();
    }

    $("#yes_button").click(yes_event);

    $("#cancel_button").click(cancel_event);
    popup.show()
}

