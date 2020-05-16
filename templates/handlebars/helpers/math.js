var helper = require('./../../js/helpers.js');

module.exports = function(firstValue, operator, secondValue, format) {
    firstValue = parseFloat(firstValue);
    secondValue = parseFloat(secondValue);

    if(operator == '/' && secondValue == 0) {
        secondValue = 1;
    }

    var mathDict = {
        "+": firstValue + secondValue,
        "-": (firstValue - secondValue),
        "*": firstValue * secondValue,
        "/": firstValue / secondValue,
        "%": firstValue % secondValue
    };

    return (format) ? helper.numberCommaFormat(mathDict[operator]) : mathDict[operator];
};