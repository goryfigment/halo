module.exports = function(x) {
    if (!(x in globals.tie)){
        globals.rank++;
        globals.tie[x] = globals.rank;
    }

    return globals.rank;
};