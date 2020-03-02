require('./../css/general.css');
require('./../css/leaderboard.css');
require('./../library/fontawesome/fontawesome.js');
require('./../library/tippy/tippy.css');

var $ = require('jquery');
var helper = require('./../js/helpers.js');
require('./../library/tippy/tippy.js');
require('./../js/general.js');

var pagination = require('./../handlebars/pagination.hbs');

var leaderboards = {
    'kills': require('./../handlebars/leaderboard/kills.hbs'),
    'deaths': require('./../handlebars/leaderboard/deaths.hbs'),
    'wins': require('./../handlebars/leaderboard/wins.hbs'),
    'losses': require('./../handlebars/leaderboard/losses.hbs'),
    'matches': require('./../handlebars/leaderboard/matches.hbs'),
    'wl': require('./../handlebars/leaderboard/wl_ratio.hbs'),
    'kd': require('./../handlebars/leaderboard/kd_ratio.hbs'),
    'playtime': require('./../handlebars/leaderboard/playtime.hbs'),
    'most_50s': require('./../handlebars/leaderboard/most_50s.hbs'),

    'h3_team_slayer': require('./../handlebars/playlist/h3_team_slayer.hbs'),
    'h3_team_hardcore': require('./../handlebars/playlist/h3_team_hardcore.hbs'),
    'h3_team_doubles': require('./../handlebars/playlist/h3_team_doubles.hbs'),
    'ms_2v2_series': require('./../handlebars/playlist/ms_2v2_series.hbs'),
    'hce_team_doubles': require('./../handlebars/playlist/hce_team_doubles.hbs'),
    'h2c_team_hardcore': require('./../handlebars/playlist/h2c_team_hardcore.hbs'),

    'halo_reach_team_hardcore': require('./../handlebars/playlist/halo_reach_team_hardcore.hbs'),
    'halo_reach_invasion': require('./../handlebars/playlist/halo_reach_invasion.hbs'),
    'halo_reach_team_slayer': require('./../handlebars/playlist/halo_reach_team_slayer.hbs')
};

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

function updateLeaderboardSuccess(response) {
    console.log('Update Success');
}

function updateLeaderboardError() {
    console.log("Leaderboard error!");
}

$(document).ready(function() {
    $('#leaderboard-wrapper').append(leaderboards[globals.type](globals.leaderboard));
    $('#pagination').append(pagination({'page': globals.page}));

    sendRequest('/update-leaderboard/', JSON.stringify({leaderboards: globals.leaderboard, type: globals.platform + globals.type, index: globals.index}), 'POST', updateLeaderboardSuccess, updateLeaderboardError);
});

$(document).on('click', '#pagination li', function () {
    window.location.replace(globals.base_url + window.location.pathname + '?page=' + $(this).text().trim());
});