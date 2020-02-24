module.exports = function(portion, total) {
    return ((portion/total) * 100).toFixed(1) + '%';
};