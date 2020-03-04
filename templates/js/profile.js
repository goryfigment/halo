require('./../css/general.css');
require('./../css/profile.css');
require('./../library/fontawesome/fontawesome.js');
require('./../library/tippy/tippy.css');

var $ = require('jquery');
var helper = require('./../js/helpers.js');
require('./../library/tippy/tippy.js');
require('./../js/general.js');

var serviceRecordTemplate = require('./../handlebars/service_record.hbs');
var playerDetailsTemplate = require('./../handlebars/player_details.hbs');
var haloRanksTemplate = require('./../handlebars/halo_ranks.hbs');
var privateTemplate = require('./../handlebars/private.hbs');
var donatorTemplate = require('./../handlebars/donator.hbs');
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
    var prevDetails = globals.player;
    $serviceRecord.empty();
    $playerDetails.empty();

    $serviceRecord.append(serviceRecordTemplate({'highest_rank': response['highest_rank'], 'gt': globals.gamertag, 'record': response}));

    response['hits'] = prevDetails['hits'];

    var change = {
        'matches': response['matches'] - prevDetails['matches'],
        'kills': response['kills'] - prevDetails['kills'],
        'deaths': response['deaths'] - prevDetails['deaths'],
        'kd': (response['kd'] - prevDetails['kd']).toFixed(2),
        'wins': response['wins'] - prevDetails['wins'],
        'losses': response['losses'] - prevDetails['losses'],
        'wl': (response['wl'] - prevDetails['wl']).toFixed(2)
    };

    $playerDetails.append(playerDetailsTemplate({'change': change, 'player': response, 'leaderboard': globals.leaderboard, 'player_count': globals.player_count}));
}

function serviceRecordError() {
    console.log("Service Record error!");
    var $leftWrapper = $('#left-wrapper');

    $leftWrapper.empty();
    $leftWrapper.append(privateTemplate({}));
}

$(document).ready(function() {
    var xbox_ranks = globals.xbox_ranks;
    var pc_ranks = globals.pc_ranks;

    var sorted_xbl_ranks = [];
    var sorted_pc_ranks = [];
    //Xbox Ranks
    for (var playlist in xbox_ranks) {
        if (xbox_ranks.hasOwnProperty(playlist)) {
            sorted_xbl_ranks.push({
                'key': helper.replaceAll(playlist.toLowerCase(), ' ', '_').replace(':', ''),
                'playlist': playlist,
                'rank': xbox_ranks[playlist][0]['SkillRank']
            });
        }
    }

    sorted_xbl_ranks.sort(function(a, b) {
        return b['rank'] - a['rank'];
    });

    var avail_pc_ranks = ['Halo: Reach Team Slayer', 'Halo: Reach Invasion', 'Halo: Reach Team Hardcore', 'HCE Hardcore Doubles'];

    //PC Ranks
    for (var pc_playlist in pc_ranks) {
        if (pc_ranks.hasOwnProperty(pc_playlist) && avail_pc_ranks.indexOf(pc_playlist) > -1) {
            sorted_pc_ranks.push({
                'key': 'pc_' + helper.replaceAll(pc_playlist.toLowerCase(), ' ', '_').replace(':', ''),
                'playlist': pc_playlist,
                'rank': pc_ranks[pc_playlist][0]['SkillRank']
            });
        }
    }

    sorted_pc_ranks.sort(function(a, b) {
        return b['rank'] - a['rank'];
    });

    globals.sorted_ranks = sorted_xbl_ranks;

    if(sorted_xbl_ranks[0]['rank'] >= sorted_pc_ranks[0]['rank']) {
        var highest_rank = sorted_xbl_ranks[0]['rank'];
    } else {
        highest_rank = sorted_pc_ranks[0]['rank'];
    }

    if(!$.isEmptyObject(globals.player)) {
        $('#service-record').append(serviceRecordTemplate({highest_rank: highest_rank, 'gt': globals.gamertag, 'record': globals.player}));
        $('#player-details').append(playerDetailsTemplate({'player': globals.player, 'leaderboard': globals.leaderboard, 'player_count': globals.player_count}));
    }

    if(globals.player['donation'] > 0) {
        var $donatorWrapper = $('#donator-wrapper');

        $donatorWrapper.append(donatorTemplate(globals.player));
        $donatorWrapper.show();
    }

    $('#xbox-rank-wrapper').append(haloRanksTemplate({'ranks': sorted_xbl_ranks, 'leaderboard': globals.leaderboard, 'player_count': globals.player_count}));
    $('#pc-rank-wrapper').append(haloRanksTemplate({'ranks': sorted_pc_ranks, 'leaderboard': globals.leaderboard, 'player_count': globals.player_count}));
    sendRequest('/service-record/', JSON.stringify({gt: globals.gamertag, xbox_ranks: xbox_ranks, pc_ranks: pc_ranks, highest_rank: highest_rank}), 'POST', serviceRecordSuccess, serviceRecordError);
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