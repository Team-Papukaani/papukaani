$(function () {
    $('a[onclick]').each(function () {
        $(this).data('onclick', this.onclick);

        this.onclick = function (event) {
            if ($(this).attr('disabled')) {
                return false;
            }

            $(this).data('onclick').call(this, event || window.event);
        };
    });
});