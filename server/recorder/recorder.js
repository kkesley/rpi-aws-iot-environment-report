const update = require('./update')
var moment = require('moment');
/**
 * query is divided into 5 parts
 * 1. Current temperature
 * 2. Hourly temperature (hash key is current hour, grouped by minutes -> maximum 60 items per hour)
 * 3. Daily temperature (hash key is current day, grouped by hours -> maximum 24 items per hour)
 * 4. Monthly temperature (hash key is current month, grouped by days -> maximum 28/29/30/31 items according to current month)
 * 5. Yearly temperature (hash key is current year, grouped by months -> maximum 12 items per year)
 */
const recorder = (table = "", event = {}) => {
    var time = moment(event.timestamp);
    if(!time.isValid()){
        return now(table, event)
    }
    //record all types of query
    return Promise.all([
        now(table, event),
        hourly(table, event, time),
        daily(table, event, time),
        monthly(table, event, time),
        yearly(table, event, time)
    ])
}
const now = (table = "", event = {}) => {
    return update(table, "now", 0, event)
}
const hourly = (table = "", event = {}, time) => {
    var timeClone = time.clone()
    //hash key as hour, grouped by minutes
    return update(table, time.startOf('hour').format("YYYY-MM-DD-HH"), timeClone.startOf('minute').valueOf(), event)
}
const daily = (table = "", event = {}, time) => {
    var timeClone = time.clone()
    //hash key as day, grouped by hours
    return update(table, time.startOf('day').format("YYYY-MM-DD"), timeClone.startOf('hour').valueOf(), event)
}
const monthly = (table = "", event = {}, time) => {
    var timeClone = time.clone()
    //hash key as month, grouped by day
    return update(table, time.startOf('month').format("YYYY-MM"), timeClone.startOf('day').valueOf(), event)
}
const yearly = (table = "", event = {}, time) => {
    var timeClone = time.clone()
    //hash key as year, grouped by month
    return update(table, time.startOf('year').format("YYYY"), timeClone.startOf('month').valueOf(), event)
}
module.exports = recorder