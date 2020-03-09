require('./../css/general.css');
require('./../css/home.css');
require('./../library/fontawesome/fontawesome.js');
require('./../library/tippy/tippy.css');

var $ = require('jquery');
var helper = require('./../js/helpers.js');
require('./../js/general.js');
require('./../library/tippy/tippy.js');

var leaderboardTemplate = require('./../handlebars/home/leaderboards.hbs');


$(document).ready(function() {
    $('#leaderboard-wrapper').append(leaderboardTemplate({mccs: globals.mccs}));
});