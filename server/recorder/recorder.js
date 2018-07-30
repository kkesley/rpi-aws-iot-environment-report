const update = require('./update')
var moment = require('moment');

const recorder = (table = "", event = {}) => {
    var time = moment(event.timestamp);
    if(!time.isValid()){
        return now(table, event)
    }
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
    return update(table, time.startOf('hour').format("YYYY-MM-DD-HH"), timeClone.startOf('minute').valueOf(), event)
}
const daily = (table = "", event = {}, time) => {
    var timeClone = time.clone()
    return update(table, time.startOf('day').format("YYYY-MM-DD"), timeClone.startOf('hour').valueOf(), event)
}
const monthly = (table = "", event = {}, time) => {
    var timeClone = time.clone()
    return update(table, time.startOf('month').format("YYYY-MM"), timeClone.startOf('day').valueOf(), event)
}
const yearly = (table = "", event = {}, time) => {
    var timeClone = time.clone()
    return update(table, time.startOf('year').format("YYYY"), timeClone.startOf('month').valueOf(), event)
}
module.exports = recorder