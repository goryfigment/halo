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
    'mccs': require('./../handlebars/leaderboard/score.hbs')
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

//function horizontalAdHandler($this) {
//    var width = $this.width();
//
//    //Fire if current size is not correct for the ad type
//    var type = $this.attr('type');
//
//    if(type == '1' && width >= 728) {
//        $this.empty();
//        $this.attr('type', 2);
//        $this.append(helper.adHandler('728x90'));
//        (adsbygoogle = window.adsbygoogle || []).push({});
//    }
//
//    if(type == '2' && width < 728) {
//        $this.empty();
//        $this.attr('type', 1);
//        $this.append(helper.adHandler('320x100'));
//        (adsbygoogle = window.adsbygoogle || []).push({});
//    }
//}
//
//function verticalAdHandler($this) {
//    var $ad = $('#right-ad');
//    var type = $ad.attr('type');
//    var width = $this.width();
//
//    //RIGHT
//    if(type == '1' && width >= 1028) { //728+300=1028 + 30 = 1058
//        $ad.empty();
//        $ad.attr('type', 2);
//        $ad.append(helper.adHandler('300x250'));
//        (adsbygoogle = window.adsbygoogle || []).push({});
//    }
//
//    if(type == '2' && width < 1028 && width >= 918) { //728+160=888 + 30 = 918
//        $ad.empty();
//        $ad.attr('type', 1);
//        $ad.append(helper.adHandler('160x600'));
//        (adsbygoogle = window.adsbygoogle || []).push({});
//    }
//
//    if(width < 888){
//        $('#right-wrapper').hide();
//    } else {
//        $('#right-wrapper').show();
//    }
//}
//
//function adStart($this, adType){
//    if(adType == 'h') {
//        //TOP AND BOTTOM
//        if($this.width() >= 728) {
//            $this.empty();
//            $this.attr('type', 2);
//            $this.append(helper.adHandler('728x90'));
//        } else {
//            $this.empty();
//            $this.attr('type', 1);
//            $this.append(helper.adHandler('320x100'));
//        }
//    } else {
//        var $ad = $('#right-ad');
//        var width = $this.width();
//
//        //RIGHT
//        if(width >= 1058) { //728+300=1028
//            $ad.empty();
//            $ad.attr('type', 2);
//            $ad.append(helper.adHandler('300x250'));
//        } else if(width < 1028 && width >= 888) { //728+160=888
//            $ad.empty();
//            $ad.attr('type', 1);
//            $ad.append(helper.adHandler('160x600'));
//        }
//
//        if(width < 888){
//            $('#right-wrapper').hide();
//        } else {
//            $('#right-wrapper').show();
//        }
//    }
//
//    (adsbygoogle = window.adsbygoogle || []).push({});
//}

$(document).ready(function() {
    $('#leaderboard-wrapper').append(leaderboards[globals.handlebars]({leaderboards: globals.leaderboard, type: globals.type.replace('s1_', '').replace('s2_', '').replace('s3_', ''), 'season': globals.season}));
    $('#pagination').append(pagination({'page': globals.page}));

    sendRequest('/update-leaderboard/', JSON.stringify({leaderboards: globals.leaderboard, type: globals.type, index: globals.index}), 'POST', updateLeaderboardSuccess, updateLeaderboardError);

    //adStart($('#top-ad'), 'h');
    //adStart($('#bottom-ad'), 'h');
    //adStart($('body'), 'v');
});

$(document).on('click', '#pagination li', function () {
    window.location.replace(globals.base_url + window.location.pathname + '?page=' + $(this).text().trim());
});

//var resizeTimeout;
//$(window).on('resize', function() {
//    clearTimeout(resizeTimeout);
//
//    resizeTimeout = setTimeout(function() {
//        horizontalAdHandler($('#top-ad'));
//        horizontalAdHandler($('#bottom-ad'));
//        verticalAdHandler($('body'));
//    }, 500);
//});