module.exports = function(type, val) {
    var trophy = {
        'playtime': [1296000, 2592000, 3888000, 5184000, 6480000],
        'mccs': [1000, 1250, 1500, 1750, 2000],
        'matches': [2000, 4000, 6000, 8000, 10000],
        'wins': [1500, 3000, 4500, 6000, 7500],
        'wl': [1.5, 2, 2.5, 3, 3.5],
        'kills': [25000, 50000, 75000, 100000, 125000],
        'kd': [1, 1.25, 1.5, 1.75, 2],
        '50': [1, 2, 3, 4, 5],
        'mvp': [500, 1000, 1500, 2000, 2500],
        'headshot': [12500, 25000, 37500, 50000, 62500],
    };

    var check = trophy[type];

    if(val < check[0]) {
        return '0';
    } else if(val >= check[0] && val < check[1]) {
        return '1';
    } else if(val >= check[1] && val < check[2]) {
        return '2';
    } else if(val >= check[2] && val < check[3]) {
        return '3';
    } else if(val >= check[3] && val < check[4]) {
        return '4';
    } else if(val >= check[4]) {
        return '5';
    }
};