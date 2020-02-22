module.exports = function(x) {
    if (!(x in globals.tie) && globals.page == 1){
        globals.rank++;
        globals.tie[x] = globals.rank;
        return globals.rank;
    } else {
        return 4;
    }
};