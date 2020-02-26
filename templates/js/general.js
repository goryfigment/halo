var $ = require('jquery');
var searchTemplate = require('./../handlebars/overlay/search.hbs');
var leaderboardTemplate = require('./../handlebars/overlay/leaderboard.hbs');

//OVERLAY//
$(document).on('click', '#overlay', function () {
    $('#overlay').removeClass('active');
});

$(document).on('keyup',function(e) {
    if (e.keyCode == 27) {
       $('#overlay').removeClass('active');
    }
});
//OVERLAY//

//SEARCH//
$(document).on('click', '#search-button', function (e) {
    e.stopPropagation();
    var $overlay = $('#overlay');
    $overlay.empty();
    $overlay.append(searchTemplate({}));
    $overlay.addClass('active');

    $('#search-input').focus();
});

$(document).on('keyup', '#search-input', function (e) {
    if (e.keyCode == 13) {
        $('#search-submit').click();
    }
});

$(document).on('click', '#search-submit', function () {
    var value = $('#search-input').val().trim();

    if(value.length != 0) {
        window.location.href = '/profile/' + value;
    }

});

$(document).on('click', '#search-container', function (e) {
    e.stopPropagation();
});
//SEARCH//

//LEADERBOARD//
$(document).on('click', '#leaderboard-button, #leaderboard', function (e) {
    e.stopPropagation();
    var $overlay = $('#overlay');
    $overlay.empty();
    $overlay.append(leaderboardTemplate({}));
    $overlay.addClass('active');
});
//LEADERBOARD//