require('./../css/general.css');
require('./../css/default.css');
require('./../library/fontawesome/fontawesome.js');
require('./../js/general.js');

var $ = require('jquery');

// TABS //
function tabHandler($tab, $wrapper) {
    $('.tab.active').removeClass('active');
    $tab.addClass('active');

    $('.active-tab').removeClass('active-tab');
    $wrapper.addClass('active-tab');
}

$(document).on('click', '.tab', function () {
    var $this = $(this);
    var $tabs = $('.tab');

    $.each( $('.tab-wrapper'), function() {
        if($this.hasClass('all-tabs')) {
            $(this).show();
        } else {
            $(this).hide();
        }
    });

    tabHandler($this, $('#' + $this.attr('data-type')));
});


// TABS //