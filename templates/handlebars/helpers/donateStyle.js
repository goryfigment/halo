module.exports = function(donate_total) {
    if(donate_total >= 100) { //disco
        return 'disco-donator';
    } else if(donate_total >= 75) { //rgb
        return 'rgb-donator';
    } else if(donate_total >= 50) { //diamond
        return 'diamond-donator';
    } else if(donate_total >= 25) { //gold
        return 'gold';
    } else if(donate_total >= 15) { //silver
        return 'silver';
    } else { //bronze
        return '#ff7d0d';
    }
};