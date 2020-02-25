module.exports = function(portion, total) {
    var percent = ((portion/total) * 100);

    if(percent < 11) { //green
        return '#04c104';
    } else if(percent < 26) { //yellow
        return '#e0d332';
    } else if(percent < 51) { //red
        return '#fd3c3c';
    } else {
        return '#a7a7a7';
    }

};