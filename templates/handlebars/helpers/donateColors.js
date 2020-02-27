module.exports = function(donate_total) {
    if(donate_total < 15) { //bronze
        return '#ff7d0d';
    } else if( donate_total >= 15 && donate_total < 25) { //silver
        return 'silver';
    } else { //gold
        return 'gold';
    }
};