require('./../css/general.css');
require('./../css/leaderboard.css');
require('./../library/fontawesome/fontawesome.js');

var $ = require('jquery');
var helper = require('./../js/helpers.js');
var mostKillsTemplate = require('./../handlebars/leaderboard/kills.hbs');

$(document).ready(function() {
    $('#leaderboard-wrapper').append(mostKillsTemplate(globals.leaderboard));
});


//SEARCH//
$(document).on('keyup', '#search', function (e) {
    if (e.keyCode == 13) {
        var $search = $(this);
        window.location.href = '/profile/' + $search.val().trim();
    }
});
//SEARCH//