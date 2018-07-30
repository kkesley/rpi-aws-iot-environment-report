const update = require('./update')
var moment = require('moment');
const now = (table = "", event = {}) => {
    return update(table, "now", event)
}
module.exports = now