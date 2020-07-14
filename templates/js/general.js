var $ = require('jquery');
var searchTemplate = require('./../handlebars/overlay/search.hbs');
var leaderboardTemplate = require('./../handlebars/overlay/leaderboard.hbs');


//ADSENSE//
//$(document).ready(function() {
//    (adsbygoogle = window.adsbygoogle || []).push({});
//});
//ADSENSE//


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

//HEADER//
$(document).on('click', '#more-button', function (e) {
    e.stopPropagation();
    $('#more-wrapper').toggleClass('active');
});

$(window).on('resize', function(){
      var win = $(this); //this = window
      if (win.width() >= 570) {
        $('#more-wrapper').removeClass('active');
      }
});
//HEADER//

function tabHandler($tab, $wrapper) {
    var $ol = $tab.closest('ol');
    var $ul = $tab.closest('ul');

    $ol.find('.tab.active').removeClass('active');
    $ul.find('.tab.active').removeClass('active');
    $tab.addClass('active');

    $wrapper.siblings('.active-tab').removeClass('active-tab');
    $wrapper.addClass('active-tab');
}

$(document).on('click', '.tab', function (e) {
    e.stopPropagation();
    var $this = $(this);
    tabHandler($this, $('#' + $this.attr('data-type')));
});