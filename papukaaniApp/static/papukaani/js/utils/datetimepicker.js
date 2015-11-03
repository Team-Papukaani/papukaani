function validateDateFormat(element) {
    var format = new RegExp("[0-3][0-9]-[0,1][0-9]-[0-9]{4} [0-2][0-9]:[0-5][0-9]");
    var val = element.value;
    if (!format.test(val) || val.length != 16) {
        element.value = "";
    }
}

$(function () {
    $.datepicker.regional['fi'] = {
        prevText: 'Edellinen',
        nextText: 'Seuraava',
        monthNames: ['Tammikuu', 'Helmikuu', 'Maaliskuu', 'Huhtikuu', 'Toukokuu', 'Kesäkuu',
            'Heinäkuu', 'Elokuu', 'Syyskuu', 'Lokakuu', 'Marraskuu', 'Joulukuu'],
        monthNamesShort: ['Tammi', 'Helmi', 'Maalis', 'Huhti', 'Touko', 'Kesä', 'Heinä',
            'Elo', 'Syys', 'Loka', 'Marras', 'Joulu'],
        dayNames: ['Sunnuntai', 'Maanantai', 'Tiistai', 'Keskiviikko', 'Torstai', 'Perjantai', 'Lauantai'],
        dayNamesMin: ['Su', 'Ma', 'Ti', 'Ke', 'To', 'Pe', 'La'],
        dateFormat: 'dd-mm-yy',
        firstDay: 1,
        isRTL: false,
        showMonthAfterYear: false,
        yearSuffix: ''
    };
    $.datepicker.setDefaults($.datepicker.regional['fi']);

    $.timepicker.regional['fi'] = {
        timeOnlyTitle: '',
        timeText: 'Aika',
        hourText: 'Tunnit',
        minuteText: 'Minuutit',
        currentText: 'Nyt',
        closeText: 'Sulje',
        timeFormat: 'HH:mm',
        isRTL: false
    };
    $.timepicker.setDefaults($.timepicker.regional['fi']);
});
