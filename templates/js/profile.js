require('./../css/general.css');
require('./../css/profile.css');
require('./../library/fontawesome/fontawesome.js');

var $ = require('jquery');
var helper = require('./../js/helpers.js');
require('./../js/general.js');

var serviceRecordTemplate = require('./../handlebars/service_record.hbs');
var playerDetailsTemplate = require('./../handlebars/player_details.hbs');
var haloRanksTemplate = require('./../handlebars/halo_ranks.hbs');
var privateTemplate = require('./../handlebars/private.hbs');
var privateTutorialTemplate = require('./../handlebars/overlay/private_tutorial.hbs');

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
    var $serviceRecord = $('#service-record');
    var $playerDetails = $('#player-details');
    $serviceRecord.empty();
    $playerDetails.empty();

    $serviceRecord.append(serviceRecordTemplate({'ranks': globals.sorted_ranks, 'gt': globals.gamertag, 'record': response, 'leaderboard': globals.leaderboard, 'player_count': globals.player_count}));

    response['hits'] = globals.player['hits'];

    $playerDetails.append(playerDetailsTemplate({'player': response, 'leaderboard': globals.leaderboard, 'player_count': globals.player_count}));
}

function serviceRecordError() {
    console.log("Service Record error!");
    var $leftWrapper = $('#left-wrapper');

    $leftWrapper.empty();
    $leftWrapper.append(privateTemplate({}));
}

$(document).ready(function() {
    var ranks = globals.ranks;
    var sorted_ranks = [];
    for (var playlist in ranks) {
        if (ranks.hasOwnProperty(playlist)) {
            sorted_ranks.push({
                'key': helper.replaceAll(playlist.toLowerCase(), ' ', '_').replace(':', ''),
                'playlist': playlist,
                'rank': ranks[playlist][0]['SkillRank']
            });
        }
    }

    sorted_ranks.sort(function(a, b) {
        return b['rank'] - a['rank'];
    });

    globals.sorted_ranks = sorted_ranks;

    if(!$.isEmptyObject(globals.player)) {
        $('#service-record').append(serviceRecordTemplate({'ranks': sorted_ranks, 'gt': globals.gamertag, 'record': globals.player}));
        $('#player-details').append(playerDetailsTemplate({'player': globals.player, 'leaderboard': globals.leaderboard, 'player_count': globals.player_count}));
    }

    $('#right-wrapper').append(haloRanksTemplate({'ranks': sorted_ranks, 'leaderboard': globals.leaderboard, 'player_count': globals.player_count}));
    sendRequest('/service-record/', JSON.stringify({gt: globals.gamertag, ranks: globals.ranks}), 'POST', serviceRecordSuccess, serviceRecordError);
});

//PRIVATE/
$(document).on('click', '#private-tutorial', function (e) {
    e.stopPropagation();
    var $overlay = $('#overlay');
    $overlay.empty();
    $overlay.append(privateTutorialTemplate({}));
    $overlay.addClass('active');
});

$(document).on('click', '#overlay img', function (e) {
    e.stopPropagation();
});
//PRIVATE//