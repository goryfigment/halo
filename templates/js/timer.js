require('./../css/general.css');
require('./../css/timer.css');
require('./../library/fontawesome/fontawesome.js');
require('./../js/general.js');

var $ = require('jquery');
var helper = require('./../js/helpers.js');

// TABS //
function tabHandler($tab, $wrapper) {
    $('.tab.active').removeClass('active');
    $tab.addClass('active');

    $('.active-tab').removeClass('active-tab');
    $wrapper.addClass('active-tab');
}

$(document).on('click', '.tab', function () {
    var $this = $(this);

    $.each( $('.tab-wrapper'), function() {
        if($this.hasClass('all-tabs')) {
            $(this).show();
        } else {
            $(this).hide();
        }
    });

    tabHandler($this, $('#' + $this.attr('data-type')));
});
// TABS //

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
    var timerTemplate = require('./../handlebars/timer/' + globals.handlebars + '.hbs');
    $('#timer-wrapper').append(timerTemplate(globals.timers));
    $($('#tabular-wrapper').find('.tab')[0]).click();

    if(globals.handlebars == 'h2_radar') {
        var $ascension = $('.ascension_sniper');
        $($ascension[0]).find('h4').text('Sniper (Main Tower)');
        $($ascension[1]).find('h4').text('Sniper (Small Tower)');

        $('.tombstone_shotgun').find('h4').text('Shotgun (Old Camo/Spiral Ramp)');
        $('.tombstone_shotgun1').find('h4').text('Shotgun (Red/Blue Bunker & Window Room)');

        $('.tombstone_overshield').find('h4').text('Overshield (Bottom Middle)');
        $('.tombstone_overshield1').find('h4').text('Overshield (Window/Long Hall)');
    }

    //adStart($('#top-ad'), 'h');
    //adStart($('#bottom-ad'), 'h');
    //adStart($('body'), 'v');
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