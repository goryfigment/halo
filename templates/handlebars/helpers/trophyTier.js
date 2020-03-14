module.exports = function(type, val) {
    var trophy = {
        'playtime': [1296000, 2592000, 3888000],
        'mccs': [1000, 1500, 2000],
        'matches': [2500,5000,7500],
        'wins': [1500, 3000, 4500],
        'wl': [1.5, 2, 2.5],
        'kills': [25000, 50000, 100000],
        'kd': [1, 1.5, 2.0],
        '50': [1, 2, 3]
    };

    var check = trophy[type];

    if(val < check[0]) {
        return '0';
    } else if(val >= check[0] && val < check[1]) {
        return '1';
    } else if(val >= check[1] && val < check[2]) {
        return '2';
    } else if(val >= check[2]) {
        return '3';
    }
};