module.exports = function(date) {
  if(date.includes('h')) {
  	var number = date.split('h')[0]
    var days = (Math.floor(Number(number) / 24)).toString()
    var hours = (Number(number) % 24)
    return days + 'd ' + date.replace(number, hours)
  } else {
  	return date
  }
};