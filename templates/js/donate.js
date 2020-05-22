require('./../css/general.css');
require('./../css/donate.css');
require('./../css/color_font.css');
require('./../library/fontawesome/fontawesome.js');
require('./../library/tippy/tippy.css');

var $ = require('jquery');
var helper = require('./../js/helpers.js');
require('./../js/general.js');
require('./../library/tippy/tippy.js');

function sendRequest(url, data, request_type, success, error, exception) {
    $.ajax({
        headers: {"X-CSRFToken": $('input[name="csrfmiddlewaretoken"]').attr('value')},
        url: globals.base_url + url,
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

function donateSuccess(response) {
    console.log('Donate Sent');
    var $formWrapper = $('#form-wrapper');
    $formWrapper.empty();
    $formWrapper.append('<h1><i class="far fa-paper-plane"></i> Message Sent</h1>');
}

function donateError() {
    console.log("Donate Error");
}

$(document).on('click', '#donate-submit', function (e) {
    e.stopPropagation();
    $('#paypal').submit();
});

$(document).on('click', '#email-submit', function (e) {
    e.stopPropagation();

    var data = {
        gamertag: $('#gamertag').val(),
        twitch: $('#twitch').val(),
        twitter: $('#twitter').val(),
        youtube: $('#youtube').val(),
        message: $('textarea').val(),
        donate: $('#donate').val(),
        color: $('#color').val(),
        discord: $('#discord').val()
    };

    sendRequest('/donate-message/', data, 'POST', donateSuccess, donateError);
});

$(document).on('click', '.donate-choice', function () {
    var $this = $(this);
    $('#choice-wrapper').find('.active').removeClass('active');
    $this.addClass('active');

    var amount = $this.text();
    if(amount != 'Custom') {
        $('#amount').val($this.text());
    } else {
        $('#amount').val('');
    }
});


//$(document).on('keyup', '#donate', function () {
//    $('#amount').val($(this).val());
//});

$(document).ready(function() {
    if(globals.t == 'true') {
        $('#thank-you-wrapper').show();
    } else {
        $('#donate-wrapper').show();
    }
});
