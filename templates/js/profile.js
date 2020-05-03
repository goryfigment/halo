require('./../css/general.css');
require('./../css/profile.css');
require('./../library/fontawesome/css/fontawesome.css');
require('./../library/tippy/tippy.css');
require('./../css/color_font.css');

var $ = require('jquery');
var helper = require('./../js/helpers.js');
require('./../js/general.js');
require('./../library/tippy/tippy.js');

var serviceRecordTemplate = require('./../handlebars/service_record.hbs');
var playerDetailsTemplate = require('./../handlebars/player_details.hbs');
var haloRanksTemplate = require('./../handlebars/halo_ranks.hbs');
var privateTemplate = require('./../handlebars/private.hbs');
var statsTemplate = require('./../handlebars/stats.hbs');
var donatorTemplate = require('./../handlebars/donator.hbs');
var fileShareTemplate = require('./../handlebars/file_share.hbs');
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
    var $statsWrapper = $('#stats-wrapper');

    var prevDetails = globals.player;
    $serviceRecord.empty();
    $playerDetails.empty();
    $statsWrapper.empty();
    $serviceRecord.append(serviceRecordTemplate({'highest_rank': response['highest_rank'], 'gt': globals.gamertag, 'record': response}));

    response['hits'] = prevDetails['hits'];

    var change = {
        'matches': response['matches'] - prevDetails['matches'],
        'kills': response['kills'] - prevDetails['kills'],
        'deaths': response['deaths'] - prevDetails['deaths'],
        'wins': response['wins'] - prevDetails['wins'],
        'losses': response['losses'] - prevDetails['losses'],
        'kd': (response['kd'] - prevDetails['kd']).toFixed(2),
        'wl': (response['wl'] - prevDetails['wl']).toFixed(2),
        'score': response['season2']['score'] - prevDetails['season2']['score'],
        's_wl': (response['season2']['wl'] - prevDetails['season2']['wl']).toFixed(2),
        's_kd': (response['season2']['kd'] - prevDetails['season2']['kd']).toFixed(2)
    };

    $playerDetails.append(playerDetailsTemplate({'change': change, 'player': response, 'leaderboard': globals.leaderboard, 'total_50s': globals.total_50s}));
    $statsWrapper.append(statsTemplate({'change': change, 'player': response, 'leaderboard': globals.leaderboard, 'player_count': globals.player_count}));

    //(adsbygoogle = window.adsbygoogle || []).push({});
}

function serviceRecordError() {
    console.log("Service Record error!");
    var $wrapper = $('#player-details');

    $wrapper.empty();
    $wrapper.append(privateTemplate({}));
}

$(document).ready(function() {
    var xbox_ranks = globals.xbox_ranks;
    var pc_ranks = globals.pc_ranks;

    var sorted_xbl_ranks = [];
    var sorted_pc_ranks = [];
    var total_50s = 0;

    //Xbox Ranks
    for (var playlist in xbox_ranks) {
        if (xbox_ranks.hasOwnProperty(playlist)) {
            var rank = xbox_ranks[playlist][0]['SkillRank'];
            sorted_xbl_ranks.push({
                'key': helper.replaceAll(playlist.toLowerCase(), ' ', '_').replace(':', ''),
                'playlist': playlist,
                'rank': rank
            });

            if(rank == 50) {
                total_50s += 1;
            }
        }
    }

    sorted_xbl_ranks.sort(function(a, b) {
        return b['rank'] - a['rank'];
    });

    var avail_pc_ranks = ['Halo: Reach Team Slayer', 'Halo: Reach Invasion', 'Halo: Reach Team Hardcore', 'HCE Hardcore Doubles'];

    //PC Ranks
    for (var pc_playlist in pc_ranks) {
        if (pc_ranks.hasOwnProperty(pc_playlist) && avail_pc_ranks.indexOf(pc_playlist) > -1) {
            rank = pc_ranks[pc_playlist][0]['SkillRank'];

            sorted_pc_ranks.push({
                'key': 'pc_' + helper.replaceAll(pc_playlist.toLowerCase(), ' ', '_').replace(':', ''),
                'playlist': pc_playlist,
                'rank': rank
            });

            if(rank == 50) {
                total_50s += 1;
            }
        }
    }

    sorted_pc_ranks.sort(function(a, b) {
        return b['rank'] - a['rank'];
    });

    globals.sorted_ranks = sorted_xbl_ranks;
    globals.total_50s = total_50s;

    if(sorted_xbl_ranks[0]['rank'] >= sorted_pc_ranks[0]['rank']) {
        var highest_rank = sorted_xbl_ranks[0]['rank'];
    } else {
        highest_rank = sorted_pc_ranks[0]['rank'];
    }

    if(!$.isEmptyObject(globals.player)) {
        $('#service-record').append(serviceRecordTemplate({highest_rank: highest_rank, 'gt': globals.gamertag, 'record': globals.player}));
        $('#player-details').append(playerDetailsTemplate({'player': globals.player, 'leaderboard': globals.leaderboard, 'total_50s': total_50s}));
        $('#stats-wrapper').append(statsTemplate({'player': globals.player, 'leaderboard': globals.leaderboard, 'player_count': globals.player_count}));
    }

    if(globals.player['donation'] > 0) {
        var $donatorWrapper = $('#donator-wrapper');
        $donatorWrapper.empty();
        $donatorWrapper.append(donatorTemplate(globals.player));
    }

    $('#xbox-rank-wrapper').append(haloRanksTemplate({'ranks': sorted_xbl_ranks, 'leaderboard': globals.leaderboard, 'player_count': globals.player_count, saved_ranks: globals.saved_ranks['xbox']}));
    $('#pc-rank-wrapper').append(haloRanksTemplate({'ranks': sorted_pc_ranks, 'leaderboard': globals.leaderboard, 'player_count': globals.player_count, saved_ranks: globals.saved_ranks['pc']}));
    sendRequest('/service-record/', JSON.stringify({gt: globals.gamertag, xbox_ranks: xbox_ranks, pc_ranks: pc_ranks, highest_rank: highest_rank}), 'POST', serviceRecordSuccess, serviceRecordError);
    sendRequest('/xbox-clips/', {gt: globals.gamertag}, 'GET', xboxClipsSuccess, xboxClipsError);
});

function xboxClipsSuccess(response) {
    //console.log(JSON.stringify(response));
    globals.clips = response;

    var $fileShare = $('#file-share-container');
    $fileShare.empty();
    $fileShare.append(fileShareTemplate({'clips': response['clips'].slice(0,6)}));
}

function xboxClipsError(response) {
    var $fileShare = $('#file-share-container');
    $fileShare.empty();
    $fileShare.append('<p>This user has no videos.</p>');
    //console.log(JSON.stringify(response));
}

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

// TABS //
function tabHandler($tab, $wrapper) {
    $('.tab.active').removeClass('active');
    $tab.addClass('active');

    $('.active-tab').removeClass('active-tab');
    $wrapper.addClass('active-tab');
}

$(document).on('click', '.tab', function () {
    var $this = $(this);
    tabHandler($this, $('#' + $this.attr('data-type')));
});
// TABS //

// FILESHARE //
$(document).on('click', '#show-all', function () {
    $('#file-share-container').append(fileShareTemplate({'clips': globals.clips['clips'].slice(6)}));
    $(this).remove();
});

$(document).on('click', '.copy-button', function () {
    var $this = $(this);
    $this.siblings('textarea').select();
    document.execCommand('copy');

    var $message = $this.siblings('.copy-message');
    $message.show();
    $message.delay(1000).fadeOut("slow");
});

//$(document).on('click play', 'video', function (e) {
//    e.stopPropagation();
//    var $this = $(this);
//    $("video").each(function() {
//        var $currentVideo = $(this);
//        if($currentVideo !== $this) {
//            $(this).get(0).pause();
//        }
//    });
//});

// FILESHARE //
