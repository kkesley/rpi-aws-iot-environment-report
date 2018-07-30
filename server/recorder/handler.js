const now = require('./now')
module.exports.hello = (event, context, callback) => {
  console.log(event)
  if(!process.env.EVENT_TABLE_NAME){
    return callback(null, "No table specified")
  }
  if(!event.temperature || !event.humidity || !event.deviceid || !event.timestamp){
    return callback(null, "invalid request");
  }
  now(process.env.EVENT_TABLE_NAME, event).then(_ => {
    return callback(null, "Success updating db")
  }).catch(_ => {
    return callback(null, "Error updating db")
  })
};
