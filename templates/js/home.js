require('./../css/general.css');
require('./../css/home.css');
require('./../library/fontawesome/fontawesome.js');
require('./../library/tippy/tippy.css');
require('./../css/color_font.css');

var $ = require('jquery');
var helper = require('./../js/helpers.js');
require('./../js/general.js');
require('./../library/tippy/tippy.js');

var leaderboardTemplate = require('./../handlebars/home/leaderboards.hbs');
var recentDonationsTemplate = require('./../handlebars/home/recent_donations.hbs');

$(document).ready(function() {
    $('#leaderboard-wrapper').append(leaderboardTemplate({mccs: globals.mccs}));
    $('#recent-donations-wrapper').append(recentDonationsTemplate(globals.recent_donations));

    var wrapper = document.getElementById('body-wrapper');
    var observer = new MutationObserver(function (mutations, observer) {
      wrapper.style.height = '';
      wrapper.style.minHeight = '';
    });
    observer.observe(wrapper, {
      attributes: true,
      attributeFilter: ['style']
    });
});


$(document).on('click', '#leaderboard-button', function () {
    $('#tip-popup').hide();
});