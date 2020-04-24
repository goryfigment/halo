require('./../css/general.css');
require('./../css/default.css');
require('./../library/fontawesome/fontawesome.js');
require('./../js/general.js');

var $ = require('jquery');

function sendRequest(url, data, request_type, success, error, exception) {
    $.ajax({
        headers: {"X-CSRFToken": $('input[name="csrfmiddlewaretoken"]').attr('value')},
        url: window.location.origin + url,
        data: data,
        dataType: 'json',
        type: request_type,
        success: function (response) {
            success(response, exception);
        },
        error: function (response) {
            error(response, exception);
        }
    });
}

// TABS //
function tabHandler($tab, $wrapper) {
    $('.tab.active').removeClass('active');
    $tab.addClass('active');

    $('.active-tab').removeClass('active-tab');
    $wrapper.addClass('active-tab');
}

$(document).on('click', '.tab', function () {
    var $this = $(this);

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

// CONTACT //
function contactSuccess(response) {
    console.log('Donate Sent');
    var $formWrapper = $('form');
    $formWrapper.empty();
    $formWrapper.append('<h1><i class="far fa-paper-plane"></i> Message Sent</h1>');
}

function contactError() {
    console.log("Contact Error");
}

$(document).on('click', '#send-message', function (e) {
    e.stopPropagation();

    var data = {
        reason: $('#reason').val(),
        gamertag: $('#gamertag').val(),
        email: $('#email').val(),
        subject: $('#subject').val(),
        message: $('#message').val()
    };

    sendRequest('/contact-message/', data, 'POST', contactSuccess, contactError);
});
// CONTACT //


$(document).ready(function() {
    if('timers' in globals) {
        var timerTemplate = require('./../handlebars/timer/' + globals.handlebars + '.hbs');
        $('#body-wrapper').append(timerTemplate(globals.timers));
        $($('#tabular-wrapper').find('.tab')[0]).click();
    }
});