const recorder = require('./recorder')
module.exports.main = (event, context, callback) => {
  console.log(event)
  //no table name. Must be specified in serverless.yml
  if(!process.env.EVENT_TABLE_NAME){
    return callback(null, "No table specified")
  }
  // validate required fields
  if((!event.temperature && event.temperature !== 0) || (!event.humidity && event.humidity !== 0) || !event.deviceid || !event.timestamp || (!event.pressure && event.pressure !== 0)){
    return callback(null, "invalid request");
  }
  //record the temperature
  recorder(process.env.EVENT_TABLE_NAME, event).then(_ => {
    return callback(null, "Success updating db")
  }).catch(_ => {
    return callback(null, "Error updating db")
  })
};
