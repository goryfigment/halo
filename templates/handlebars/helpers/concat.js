module.exports = function() {
    var outStr = '';
    for(var arg in arguments){
        if(typeof arguments[arg]!='object'){
            if(arguments[arg] == 'base_url') {
                arguments[arg] = globals.base_url;
            }
            outStr += arguments[arg];
        }
    }
    return outStr;
};