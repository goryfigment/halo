require('./../css/general.css');
require('./../css/donate.css');
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
}

function donateError() {
    console.log("Donate Error");
}

$(document).on('click', '#donate-submit', function (e) {
    e.stopPropagation();

    var data = {
        gamertag: $('#gamertag').val(),
        twitch: $('#twitch').val(),
        twitter: $('#twitter').val(),
        youtube: $('#youtube').val(),
        message: $('textarea').val(),
        donate: $('#donate').val()
    };

    $('#paypal').submit();

    sendRequest('/donate-message/', data, 'POST', donateSuccess, donateError);
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
