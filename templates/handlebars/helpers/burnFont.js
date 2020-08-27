var $ = require('jquery');
var Handlebars = require('handlebars');

module.exports = function(gt) {
    var gamertag = $.map((gt + '').split(''), function(n, i) {
        if(i%2 == 0) {
            return '<span class="fire">'+ n + '</span>';
        } else {
            return '<span class="burn">'+ n + '</span>';
        }
    });

    return new Handlebars.SafeString(String(gamertag).replace(new RegExp(','.replace(/([.*+?^=!:${}()|\[\]\/\\])/g, "\\$1"), 'g'), ''));
};