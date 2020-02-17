require('./../css/general.css');
require('./../css/profile.css');
require('./../library/fontawesome/fontawesome.js');

var $ = require('jquery');
var helper = require('./../js/helpers.js');

var profileTemplate = require('./../handlebars/profile.hbs');

$(document).ready(function() {
    $('#wrapper').append(profileTemplate({'ranks': globals.ranks, 'gt': globals.gamertag}));

});

//SEARCH//
$(document).on('keyup', '#search', function (e) {
    if (e.keyCode == 13) {
        var $search = $(this);
        window.location.href = '/profile/' + $search.val().trim();
    }
});
//SEARCH//