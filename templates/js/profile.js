require('./../css/general.css');
require('./../css/profile.css');
require('./../library/fontawesome/css/fontawesome.css');
require('./../library/tippy/tippy.css');
require('./../css/color_font.css');

var $ = require('jquery');
var helper = require('./../js/helpers.js');
require('./../js/general.js');
require('./../library/tippy/tippy.js');

var serviceRecordTemplate = require('./../handlebars/profile/service_record.hbs');
var playerDetailsTemplate = require('./../handlebars/profile/player_details.hbs');
var haloRanksTemplate = require('./../handlebars/profile/halo_ranks.hbs');
var privateTemplate = require('./../handlebars/profile/private.hbs');
var statsTemplate = require('./../handlebars/profile/stats.hbs');
var donatorTemplate = require('./../handlebars/profile/donator.hbs');
var fileShareTemplate = require('./../handlebars/profile/file_share.hbs');
var matchesTemplate = require('./../handlebars/profile/matches.hbs');
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
        'assists': response['assists'] - prevDetails['assists'],
        'betrayals': response['betrayals'] - prevDetails['betrayals'],
        'headshots': response['headshots'] - prevDetails['headshots'],
        'matches': response['matches'] - prevDetails['matches'],
        'kills': response['kills'] - prevDetails['kills'],
        'deaths': response['deaths'] - prevDetails['deaths'],
        'wins': response['wins'] - prevDetails['wins'],
        'losses': response['losses'] - prevDetails['losses'],
        'kd': (response['kd'] - prevDetails['kd']).toFixed(2),
        'wl': (response['wl'] - prevDetails['wl']).toFixed(2),
        'score': response['season4']['score'] - prevDetails['season4']['score'],
        's_wl': (response['season4']['wl'] - prevDetails['season4']['wl']).toFixed(2),
        's_kd': (response['season4']['kd'] - prevDetails['season4']['kd']).toFixed(2)
    };

    $playerDetails.append(playerDetailsTemplate({'change': change, 'player': response, 'leaderboard': globals.leaderboard, 'total_50s': globals.total_50s}));
    $statsWrapper.append(statsTemplate({'change': change, 'player': response, 'leaderboard': globals.leaderboard, 'player_count': globals.player_count}));

    console.log(JSON.stringify(response));

    //(adsbygoogle = window.adsbygoogle || []).push({});
}

function emblemSuccess(response) {
    console.log('Emblem updated: ' + response["emblem"]);

    $("#emblem").attr("src", response["emblem"]);
}

function emblemError() {
    console.log('Emblem error');
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
            var key = helper.replaceAll(playlist.toLowerCase(), ' ', '_').replace(':', '');

            sorted_xbl_ranks.push({
                'key': key,
                'playlist': playlist,
                'rank': rank,
                'leaderboard': globals.leaderboard['new_' + key],
                'verified': globals.saved_ranks['xbox']['v_' + key]
            });

            if(rank == 50) {
                total_50s += 1;
            }
        }
    }

    sorted_xbl_ranks.sort(function(a, b) {
        return b['rank'] - a['rank'];
    });

    //var avail_pc_ranks = ['Halo: Reach Team Slayer', 'Halo: Reach Invasion', 'Halo: Reach Team Hardcore', 'HCE Hardcore Doubles', 'H2C Team Hardcore', 'H2A Team Hardcore'];

    //PC Ranks
    for (var pc_playlist in pc_ranks) {
        if (pc_ranks.hasOwnProperty(pc_playlist)/* && avail_pc_ranks.indexOf(pc_playlist) > -1*/) {
            rank = pc_ranks[pc_playlist][0]['SkillRank'];
            key = helper.replaceAll(pc_playlist.toLowerCase(), ' ', '_').replace(':', '');

            sorted_pc_ranks.push({
                'key': key,
                'playlist': pc_playlist,
                'rank': rank,
                'leaderboard': globals.leaderboard['new_pc_' + key],
                'verified': globals.saved_ranks['pc']['v_' + key]
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
        //$donatorWrapper.empty();
        $donatorWrapper.prepend(donatorTemplate(globals.player));
    }

    $('#xbox-rank-wrapper').append(haloRanksTemplate({'ranks': sorted_xbl_ranks, 'player_count': globals.player_count}));
    $('#pc-rank-wrapper').append(haloRanksTemplate({'ranks': sorted_pc_ranks, 'player_count': globals.player_count}));
    sendRequest('/service-record/', JSON.stringify({gt: globals.gamertag, xbox_ranks: xbox_ranks, pc_ranks: pc_ranks, highest_rank: highest_rank}), 'POST', serviceRecordSuccess, serviceRecordError);
    sendRequest('/player-matches/', {'gt': globals.gamertag, 'game_variant': '', 'req': 6}, 'GET', playerMatchesSuccess, playerMatchesError);
    sendRequest('/xbox-clips/', {gt: globals.gamertag}, 'GET', xboxClipsSuccess, xboxClipsError);
    sendRequest('/update-emblem/', {gt: globals.gamertag}, 'GET', emblemSuccess, emblemError);

    //OLD RANKS//
    prevRankshandler(globals.old_saved_ranks['xbox'], globals.old_saved_ranks['pc']);
    //OLD RANKS//
});

function prevRankshandler(xbox_ranks, pc_ranks) {
    var xbox_keys = ["ms_2v2_series", "hce_hardcore_doubles", "h2a_team_hardcore", "h3_team_doubles", "h3_team_slayer", "h2c_team_hardcore", "halo_reach_team_slayer", "halo_reach_team_hardcore", "hce_team_doubles", "h3_team_hardcore", "halo_reach_invasion"];
    var pc_keys = ["h2c_team_hardcore", "hce_hardcore_doubles", "halo_reach_team_hardcore", "h2a_team_hardcore", "halo_reach_invasion", "halo_reach_team_slayer"];

    var old_xbox_ranks = [];
    var old_pc_ranks = [];

    for (var i = 0; i < xbox_keys.length; i++) {
        var key = xbox_keys[i];
        var playlist_name = helper.replaceAll(key, '_', ' ').replace('halo reach', 'halo: reach').replace('h2a', 'H2A').replace('hce', 'HCE').replace('ms', 'MS').replace('h2c', 'H2C');
        old_xbox_ranks.push({
            'key': key,
            'playlist': playlist_name,
            'rank': xbox_ranks[key],
            'leaderboard': globals.leaderboard['old_' + key],
            'verified': xbox_ranks['v_' + key]
        });
    }

    old_xbox_ranks.sort(function(a, b) {
        return b['rank'] - a['rank'];
    });

    for (var p = 0; p < pc_keys.length; p++) {
        key = pc_keys[p];
        playlist_name = helper.replaceAll(key, '_', ' ').replace('halo reach', 'halo: reach').replace('h2a', 'H2A').replace('hce', 'HCE').replace('h2c', 'H2C');
        old_pc_ranks.push({
            'key': key,
            'playlist': playlist_name,
            'rank': pc_ranks[key],
            'leaderboard': globals.leaderboard['old_pc_' + key],
            'verified': pc_ranks['v_' + key]
        });
    }

    old_pc_ranks.sort(function(a, b) {
        return b['rank'] - a['rank'];
    });

    $('#prev-xbox-rank-wrapper').append(haloRanksTemplate({'ranks': old_xbox_ranks, 'player_count': globals.player_count}));
    $('#prev-pc-rank-wrapper').append(haloRanksTemplate({'ranks': old_pc_ranks, 'player_count': globals.player_count}));
}

function playerMatchesSuccess(response) {
    var $wrapper = $('#matches-wrapper');
    $wrapper.empty();
    $wrapper.append(matchesTemplate({'sessions': splitSessions(response['matches'])}));
}

function playerMatchesError(response) {
    console.log("Player Matches error!");
}

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
//function tabHandler($tab, $wrapper) {
//    var $ol = $tab.closest('ol');
//
//    $ol.find('.tab.active').removeClass('active');
//    $tab.addClass('active');
//
//    $wrapper.siblings('.active-tab').removeClass('active-tab');
//    $wrapper.addClass('active-tab');
//}
//
//$(document).on('click', '.tab', function (e) {
//    e.stopPropagation();
//    var $this = $(this);
//    tabHandler($this, $('#' + $this.attr('data-type')));
//});
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

function splitSessions(matches) {
    var sessionsList = [];
    var currentDict = {};
    var currentList = [];

    var kills = 0;
    var deaths = 0;
    var assists = 0;
    var wins = 0;
    var losses = 0;

    for (var i = 0; i < matches.length; i++) {
        var currentMatch = matches[i];
        //Add to session
        currentList.push(currentMatch);
        kills += currentMatch['Kills'];
        deaths += currentMatch['Deaths'];
        assists += currentMatch['Assists'];

        if(currentMatch['Won']) {
            wins += 1;
        }  else {
            losses += 1;
        }

        if(i+1 < matches.length) {
            var nextMatch = matches[i+1]
        }

        if(nextMatch != undefined) {
            var firstMatch = Math.floor(new Date(currentMatch['DateTime']).getTime()/ 1000);
            var secondMatch = Math.floor(new Date(nextMatch['DateTime']).getTime() / 1000);
            var difference = firstMatch - secondMatch;

            if(difference > 3600) {
                currentDict['session'] = currentList;
                currentDict['kills'] = kills;
                currentDict['deaths'] = deaths;
                currentDict['assists'] = assists;
                currentDict['wins'] = wins;
                currentDict['losses'] = losses;
                currentDict['wl_ratio'] = Math.floor(parseFloat(wins)/parseFloat(wins+losses)*100);
                currentDict['kad'] = (parseFloat(kills + assists)/parseFloat(deaths)).toFixed(2);
                sessionsList.push(currentDict);

                currentList = [];
                currentDict = {};
                kills = 0;
                deaths = 0;
                assists = 0;
                wins = 0;
                losses = 0;
            }
        }
    }

    return sessionsList;
}

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
