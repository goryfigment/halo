require('./../css/general.css');
require('./../css/home.css');
require('./../library/fontawesome/fontawesome.js');

var $ = require('jquery');
var helper = require('./../js/helpers.js');

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

//SEARCH//
$(document).on('keyup', '#search', function (e) {
    if (e.keyCode == 13) {
        var $search = $(this);
        window.location.href = '/profile/' + $search.val().trim();
    }
});
//SEARCH//

