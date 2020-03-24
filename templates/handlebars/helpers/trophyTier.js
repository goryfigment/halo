module.exports = function(type, val) {
    var trophy = {
        'playtime': [1296000, 2592000, 3888000, 5184000],
        'mccs': [1000, 1500, 2000, 2500],
        'matches': [2500, 5000, 7500, 10000],
        'wins': [1500, 3000, 4500, 6000],
        'wl': [1.5, 2, 2.5, 3],
        'kills': [25000, 50000, 75000, 100000],
        'kd': [1, 1.5, 2.0, 2.5],
        '50': [1, 2, 3, 4]
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
    } else if(val >= check[3]) {
        return '4';
    }
};