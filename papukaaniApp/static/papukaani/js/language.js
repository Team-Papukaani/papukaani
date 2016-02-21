var assert = function(condition, message) { 
    if (!condition) {
          debugger;
              throw Error("Assert failed" + (typeof message !== "undefined" ? ": " + message : ""));
                }
};

$(function () {
  var currentLang = $('#language_choose').attr('data-currentlang');
  assert(currentLang.length === 2);

  $('#language_choose .language_option').each(function (i, el) {
    var el = $(el);
    var langcode = el.attr('data-langcode');
    if (langcode === currentLang) {
      el.addClass('language_current');
    }
    $(el).click(function (event) {
      event.preventDefault();
      $('#language_form_select').val(langcode);
      $('#language_form').submit();
    });
  });
});
