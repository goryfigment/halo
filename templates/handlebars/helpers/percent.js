module.exports = function(portion, total) {
    var percent = ((portion/total) * 100).toFixed(1) + '%';
    return percent == '0.0%' ? '0.1%' : percent;
};