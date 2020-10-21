require('./../css/general.css');
require('./../css/home.css');
require('./../library/fontawesome/fontawesome.js');
require('./../library/tippy/tippy.css');
require('./../css/color_font.css');

var $ = require('jquery');
var helper = require('./../js/helpers.js');
require('./../js/general.js');
require('./../library/tippy/tippy.js');

var mccsTemplate = require('./../handlebars/home/leaderboards.hbs');
var playtimeTemplate = require('./../handlebars/home/playtime.hbs');
var playlistTemplate = require('./../handlebars/home/playlist.hbs');
var leaderboardTemplate = require('./../handlebars/home/s1_leaderboard.hbs');
var recentDonationsTemplate = require('./../handlebars/home/recent_donations.hbs');
var populationTemplate = require('./../handlebars/home/population.hbs');


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


$(document).ready(function() {
    $('#recent-donations-wrapper').append(recentDonationsTemplate(globals.recent_donations));

    //RANK LEADERBOARDS
    $('#pc-h3-recon-wrapper').append(playlistTemplate({leaderboards: globals.pc_h3_recon_slayer}));
    $('#pc-h3-slayer-wrapper').append(playlistTemplate({leaderboards: globals.pc_h3_team_slayer}));
    $('#pc-h3-hardcore-wrapper').append(playlistTemplate({leaderboards: globals.pc_h3_team_hardcore}));
    $('#pc-h3-dubs-wrapper').append(playlistTemplate({leaderboards: globals.pc_h3_team_doubles}));
    $('#pc-h2a-hardcore-wrapper').append(playlistTemplate({leaderboards: globals.pc_h2a_team_hardcore}));
    $('#pc-h2c-hardcore-wrapper').append(playlistTemplate({leaderboards: globals.pc_h2c_team_hardcore}));
    $('#pc-h1-hardcore-wrapper').append(playlistTemplate({leaderboards: globals.pc_hce_hardcore_doubles}));
    $('#pc-reach-invasion-wrapper').append(playlistTemplate({leaderboards: globals.pc_halo_reach_invasion}));
    $('#pc-reach-hardcore-wrapper').append(playlistTemplate({leaderboards: globals.pc_halo_reach_team_hardcore}));

    $('#h3-recon-wrapper').append(playlistTemplate({leaderboards: globals.h3_recon_slayer}));
    $('#h3-slayer-wrapper').append(playlistTemplate({leaderboards: globals.h3_team_slayer}));
    $('#h3-hardcore-wrapper').append(playlistTemplate({leaderboards: globals.h3_team_hardcore}));
    $('#h3-dubs-wrapper').append(playlistTemplate({leaderboards: globals.h3_team_doubles}));
    $('#h2a-hardcore-wrapper').append(playlistTemplate({leaderboards: globals.h2a_team_hardcore}));
    $('#h2c-hardcore-wrapper').append(playlistTemplate({leaderboards: globals.h2c_team_hardcore}));
    $('#h1-hardcore-wrapper').append(playlistTemplate({leaderboards: globals.hce_hardcore_doubles}));
    $('#reach-invasion-wrapper').append(playlistTemplate({leaderboards: globals.halo_reach_invasion}));
    $('#reach-hardcore-wrapper').append(playlistTemplate({leaderboards: globals.halo_reach_team_hardcore}));

    getPopulation();
    //S5 LEADERBOARDS
    $('#mccs-wrapper').append(mccsTemplate({mccs: globals.mccs}));
    $('#playtime-wrapper').append(playtimeTemplate({leaderboards: globals.playtime, type: 'playtime'}));
    $('#kills-wrapper').append(leaderboardTemplate({leaderboards: globals.kills, type: 'kills'}));
    $('#deaths-wrapper').append(leaderboardTemplate({leaderboards: globals.deaths, type: 'deaths'}));
    $('#wins-wrapper').append(leaderboardTemplate({leaderboards: globals.wins, type: 'wins'}));
    $('#losses-wrapper').append(leaderboardTemplate({leaderboards: globals.losses, type: 'losses'}));
    $('#matches-wrapper').append(leaderboardTemplate({leaderboards: globals.matches, type: 'matches'}));
    $('#kd-wrapper').append(leaderboardTemplate({leaderboards: globals.kd, type: 'kd'}));
    $('#wl-wrapper').append(leaderboardTemplate({leaderboards: globals.wl, type: 'wl'}));
    $('#assists-wrapper').append(leaderboardTemplate({leaderboards: globals.assists, type: 'assists'}));
    $('#betrayals-wrapper').append(leaderboardTemplate({leaderboards: globals.betrayals, type: 'betrayals'}));
    $('#headshots-wrapper').append(leaderboardTemplate({leaderboards: globals.headshots, type: 'headshots'}));

    //(adsbygoogle = window.adsbygoogle || []).push({});
});

$(document).on('click', '#leaderboard-button', function () {
    $('#tip-popup').hide();
});

function getPopulation() {
    sendRequest("/halo-population/", {}, "GET", success, error);

    function success(response) {
        $('#population-wrapper').append(populationTemplate(response));
    }

    function error(response) {
        console.log(JSON.stringify(response));
    }
}

// TABS //
//function tabHandler($tab, $wrapper) {
//    $('.tab.active').removeClass('active');
//    $tab.addClass('active');
//
//    $('.active-tab').removeClass('active-tab');
//    $wrapper.addClass('active-tab');
//}
//
//$(document).on('click', '.tab', function () {
//    var $this = $(this);
//    tabHandler($this, $('#' + $this.attr('data-type')));
//});
// TABS //