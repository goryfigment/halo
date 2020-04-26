require('./../css/general.css');
require('./../css/resources.css');
require('./../library/fontawesome/fontawesome.js');
require('./../js/general.js');

var $ = require('jquery');
var helper = require('./../js/helpers.js');

function horizontalAdHandler($this) {
    var width = $this.width();

    //Fire if current size is not correct for the ad type
    var type = $this.attr('type');

    if(type == '1' && width >= 728) {
        $this.empty();
        $this.attr('type', 2);
        $this.append(helper.adHandler('728x90'));
        (adsbygoogle = window.adsbygoogle || []).push({});
    }

    if(type == '2' && width < 728) {
        $this.empty();
        $this.attr('type', 1);
        $this.append(helper.adHandler('320x100'));
        (adsbygoogle = window.adsbygoogle || []).push({});
    }
}

function verticalAdHandler($this) {
    var $ad = $('#right-ad');
    var type = $ad.attr('type');
    var width = $this.width();

    //RIGHT
    if(type == '1' && width >= 1028) { //728+300=1028 + 30 = 1058
        $ad.empty();
        $ad.attr('type', 2);
        $ad.append(helper.adHandler('300x250'));
        (adsbygoogle = window.adsbygoogle || []).push({});
    }

    if(type == '2' && width < 1028 && width >= 918) { //728+160=888 + 30 = 918
        $ad.empty();
        $ad.attr('type', 1);
        $ad.append(helper.adHandler('160x600'));
        (adsbygoogle = window.adsbygoogle || []).push({});
    }

    if(width < 888){
        $('#right-wrapper').hide();
    } else {
        $('#right-wrapper').show();
    }
}

function adStart($this, adType){
    if(adType == 'h') {
        //TOP AND BOTTOM
        if($this.width() >= 728) {
            $this.empty();
            $this.attr('type', 2);
            $this.append(helper.adHandler('728x90'));
        } else {
            $this.empty();
            $this.attr('type', 1);
            $this.append(helper.adHandler('320x100'));
        }
    } else {
        var $ad = $('#right-ad');
        var width = $this.width();

        //RIGHT
        if(width >= 1058) { //728+300=1028
            $ad.empty();
            $ad.attr('type', 2);
            $ad.append(helper.adHandler('300x250'));
        } else if(width < 1028 && width >= 888) { //728+160=888
            $ad.empty();
            $ad.attr('type', 1);
            $ad.append(helper.adHandler('160x600'));
        }

        if(width < 888){
            $('#right-wrapper').hide();
        } else {
            $('#right-wrapper').show();
        }
    }

    (adsbygoogle = window.adsbygoogle || []).push({});
}

$(document).ready(function() {
    adStart($('#top-ad'), 'h');
    adStart($('#bottom-ad'), 'h');
    adStart($('body'), 'v');
});

$(document).on('click', '#pagination li', function () {
    window.location.replace(globals.base_url + window.location.pathname + '?page=' + $(this).text().trim());
});

var resizeTimeout;
$(window).on('resize', function() {
    clearTimeout(resizeTimeout);

    resizeTimeout = setTimeout(function() {
        horizontalAdHandler($('#top-ad'));
        horizontalAdHandler($('#bottom-ad'));
        verticalAdHandler($('body'));
    }, 500);
});