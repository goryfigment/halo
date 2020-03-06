var helper = require('./../../js/helpers.js');
module.exports = function(x) {
    if(x >= 1000) {
        return helper.numberCommaFormat(x);
    } else {
        return x;
    }
};