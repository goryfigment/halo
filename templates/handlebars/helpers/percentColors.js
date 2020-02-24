module.exports = function(portion, total) {
    var percent = ((portion/total) * 100);

    if(percent < 11) { //green
        return '#04c104';
    } else if(percent < 26) { //yellow
        return '#cde032';
    } else if(percent < 51) { //red
        return '#fd3c3c';
    } else {
        return '#ffffff';
    }

};