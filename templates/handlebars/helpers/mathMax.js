var helper = require('./../../js/helpers.js');

module.exports = function(firstValue, operator, secondValue, max) {
    firstValue = parseFloat(firstValue);
    secondValue = parseFloat(secondValue);

    var mathDict = {
        "+": firstValue + secondValue,
        "-": (firstValue - secondValue),
        "*": firstValue * secondValue,
        "/": firstValue / secondValue,
        "%": firstValue % secondValue
    };

    var value = mathDict[operator];

    return (value > max) ? max : mathDict[operator];
};