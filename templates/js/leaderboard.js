require('./../css/general.css');
require('./../css/leaderboard.css');
require('./../library/fontawesome/fontawesome.js');

var $ = require('jquery');
var helper = require('./../js/helpers.js');
require('./../js/general.js');

var pagination = require('./../handlebars/pagination.hbs');

var leaderboards = {
    'most_kills': require('./../handlebars/leaderboard/kills.hbs'),
    'most_deaths': require('./../handlebars/leaderboard/deaths.hbs'),
    'most_wins': require('./../handlebars/leaderboard/wins.hbs'),
    'most_losses': require('./../handlebars/leaderboard/losses.hbs'),
    'most_matches': require('./../handlebars/leaderboard/matches.hbs'),
    'best_wl': require('./../handlebars/leaderboard/wl_ratio.hbs'),
    'best_kd': require('./../handlebars/leaderboard/kd_ratio.hbs'),
    'most_playtime': require('./../handlebars/leaderboard/playtime.hbs'),
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

$(document).ready(function() {
    $('#leaderboard-wrapper').append(leaderboards[globals.type](globals.leaderboard));
    $('#pagination').append(pagination({'page': globals.page}));
});

$(document).on('click', '#pagination li', function () {
    console.log(globals.base_url)

    window.location.replace(globals.base_url + window.location.pathname + '?page=' + $(this).text().trim());
});