require('./../css/general.css');
require('./../css/leaderboard.css');
require('./../library/fontawesome/fontawesome.js');
require('./../library/tippy/tippy.css');
require('./../css/color_font.css');

var $ = require('jquery');
var helper = require('./../js/helpers.js');
require('./../library/tippy/tippy.js');
require('./../js/general.js');

var pagination = require('./../handlebars/pagination.hbs');

var leaderboards = {
    'playtime': require('./../handlebars/leaderboard/playtime.hbs'),
    'most_50s': require('./../handlebars/leaderboard/most_50s.hbs'),
    'season1': require('./../handlebars/leaderboard/season1.hbs'),
    'season1_ratio': require('./../handlebars/leaderboard/season1_ratio.hbs'),
    'player': require('./../handlebars/leaderboard/player.hbs'),
    'player_ratio': require('./../handlebars/leaderboard/player_ratio.hbs'),
    'playlist': require('./../handlebars/leaderboard/playlist.hbs'),
    'mccs': require('./../handlebars/leaderboard/score.hbs'),
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
    $('#leaderboard-wrapper').append(leaderboards[globals.handlebars]({leaderboards: globals.leaderboard, type: globals.type.replace('s1_', '')}));
    $('#pagination').append(pagination({'page': globals.page}));

    sendRequest('/update-leaderboard/', JSON.stringify({leaderboards: globals.leaderboard, type: globals.type, index: globals.index}), 'POST', updateLeaderboardSuccess, updateLeaderboardError);
});

$(document).on('click', '#pagination li', function () {
    window.location.replace(globals.base_url + window.location.pathname + '?page=' + $(this).text().trim());
});