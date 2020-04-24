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
var leaderboardTemplate = require('./../handlebars/home/s1_leaderboard.hbs');
var recentDonationsTemplate = require('./../handlebars/home/recent_donations.hbs');

$(document).ready(function() {
    $('#recent-donations-wrapper').append(recentDonationsTemplate(globals.recent_donations));

    //S1 LEADERBOARDS
    $('#mccs-wrapper').append(mccsTemplate({mccs: globals.mccs}));
    $('#playtime-wrapper').append(playtimeTemplate({leaderboards: globals.playtime, type: 'playtime'}));
    $('#kills-wrapper').append(leaderboardTemplate({leaderboards: globals.kills, type: 'kills'}));
    $('#deaths-wrapper').append(leaderboardTemplate({leaderboards: globals.deaths, type: 'deaths'}));
    $('#wins-wrapper').append(leaderboardTemplate({leaderboards: globals.wins, type: 'wins'}));
    $('#losses-wrapper').append(leaderboardTemplate({leaderboards: globals.losses, type: 'losses'}));
    $('#matches-wrapper').append(leaderboardTemplate({leaderboards: globals.matches, type: 'matches'}));
    $('#kd-wrapper').append(leaderboardTemplate({leaderboards: globals.kd, type: 'kd'}));
    $('#wl-wrapper').append(leaderboardTemplate({leaderboards: globals.wl, type: 'wl'}));

    $("#ad-wrapper").each(function () {
        $(this).append('<ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-1676522332244979" data-ad-slot="3635508703" data-ad-format="auto" data-full-width-responsive="true"></ins>');
        (adsbygoogle = window.adsbygoogle || []).push({});
    });
});

$(document).on('click', '#leaderboard-button', function () {
    $('#tip-popup').hide();
});

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