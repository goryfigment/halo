module.exports = function(d, dateOnly) {
    return dateOnly ? (new Date(d)).toLocaleDateString() : (new Date(d)).toLocaleString();
};