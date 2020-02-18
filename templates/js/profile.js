require('./../css/general.css');
require('./../css/profile.css');
require('./../library/fontawesome/fontawesome.js');

var $ = require('jquery');
var helper = require('./../js/helpers.js');

var serviceRecordTemplate = require('./../handlebars/service_record.hbs');
var playerDetailsTemplate = require('./../handlebars/player_details.hbs');
var haloRanksTemplate = require('./../handlebars/halo_ranks.hbs');
var privateTemplate = require('./../handlebars/private.hbs');

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

function serviceRecordSuccess(response) {
    console.log(JSON.stringify(response));

    $('#service-record').append(serviceRecordTemplate({'ranks': globals.ranks, 'gt': globals.gamertag, 'record': response}));
    $('#player-details').append(playerDetailsTemplate(response));
}

function serviceRecordError() {
    console.log("Service Record error!");
    var $leftWrapper = $('#left-wrapper');

    $leftWrapper.empty();
    $leftWrapper.append(privateTemplate({}));
}

$(document).ready(function() {
    //$('#wrapper').append(profileTemplate({'ranks': globals.ranks, 'gt': globals.gamertag}));
    $('#right-wrapper').append(haloRanksTemplate(globals.ranks));
    sendRequest('/service-record/', {gt: globals.gamertag}, 'GET', serviceRecordSuccess, serviceRecordError);
});

//SEARCH//
$(document).on('keyup', '#search', function (e) {
    if (e.keyCode == 13) {
        var $search = $(this);
        window.location.href = '/profile/' + $search.val().trim();
    }
});
//SEARCH//

//PRIVATE/
$(document).on('click', '#private-tutorial', function (e) {
    e.stopPropagation();
    $('#overlay').addClass('active');
});

$(document).on('click', '#overlay img', function (e) {
    e.stopPropagation();
});

$(document).on('click', '#overlay', function (e) {
    $('#overlay').removeClass('active');
});
//PRIVATE//