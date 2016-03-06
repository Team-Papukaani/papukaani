var assert = function (condition, message) {
    if (!condition) {
        throw Error("Assert failed" + (typeof message !== "undefined" ? ": " + message : ""));
    }
};

var removeParamFromUrl = function (url, param) {
    var queryString = (url.indexOf('?') >= 0) ? url.split('?')[1] : '';
    if (queryString === '') {
        return url;
    }

    var params = queryString.split('&');
    for (var i = 0; i < params.length; i++) {
        var thisParam = params[i].split('=')[0];
        if (thisParam === param) {
            params.splice(i, 1);
        }
    }
    var start = url.split('?')[0];
    return start + '?' + params.join('&');
};

$(function () {
    if ($('#language_choose').length) {
        var currentLang = $('#language_choose').attr('data-currentlang');
        assert(currentLang.length === 2);
        var currentFullUrl = $('#language_form').attr('data-currentfullurl');
        assert(!!currentFullUrl);

        $('#language_choose .language_option').each(function (i, el) {
            var el = $(el);
            var langcode = el.attr('data-langcode');
            if (langcode === currentLang) {
                el.addClass('language_current');
            }
            $(el).click(function (event) {
                event.preventDefault();
                $('#language_form_next').val(
                    removeParamFromUrl(currentFullUrl, 'lang'));
                $('#language_form_select').val(langcode);
                $('#language_form').submit();
            });
        });
    }
});
