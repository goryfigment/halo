var $ = require('jquery');
var Handlebars = require('handlebars');

module.exports = function(gt) {
    var gamertag = $.map((gt + '').split(''), function(n, i) {
        return '<span>'+ n + '</span>';
    });

    return new Handlebars.SafeString('<span class="anim-text-flow">' + (String(gamertag).replace(new RegExp(','.replace(/([.*+?^=!:${}()|\[\]\/\\])/g, "\\$1"), 'g'), '')) + '</span>');
};