module.exports = function(time) {
    var created = new Date(time).getTime()/ 1000;
    var now = Math.floor(new Date().getTime() / 1000);
    var difference = now - created;
    //              min hr    day    week    month    year
    var timespan = [60, 3600, 86400, 604800, 2628000, 31536000];

    if(difference < timespan[0]) { //If less then 1 minute
        return 'now';
    } else if(difference >= timespan[0] && difference < timespan[1]) { //If >= 1 minute and < hour
        var min = String(Math.floor(difference / 60));
        var string = min + ' min';
        return (min > 1) ? string + 's' : string;
    } else if(difference >= timespan[1] && difference < timespan[2]) { //If >= 1 hour and < day
        var hour = String(Math.floor(difference / 3600));
        string = hour + ' hour';
        return (hour > 1) ? string + 's' : string;
    } else if(difference >= timespan[2] && difference < timespan[3]) { //If >= 1 day and < week
        var day = String(Math.floor(difference / 86400));
        string = day + ' day';
        return (day > 1) ? string + 's' : string;
    } else if(difference >= timespan[3] && difference < timespan[4]) { //If >= 1 week and < month
        var week = String(Math.floor(difference / 604800));
        string = week + ' week';
        return (week > 1) ? string + 's' : string;
    } else if(difference >= timespan[4] && difference < timespan[5]) { //If >= 1 month and < year
        var month = String(Math.floor(difference / 2628000));
        string = month + ' month';
        return (month > 1) ? string + 's' : string;
    } else if(difference >= timespan[5]) { //If >= 1 year
        var year = String(Math.floor(difference / 31536000));
        string = year + ' year';
        return (year > 1) ? string + 's' : string;
    }
};