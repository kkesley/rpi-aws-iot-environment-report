const moment = require('moment-timezone')
const query = require('./query')
module.exports.main = (event, context, callback) => {
    console.log(event)
    //no table name. Must be specified in serverless.yml
    if(!process.env.EVENT_TABLE_NAME){
        return callback(null, "No table specified")
    }
    // construct key by date for dynamoDB key
    var groupingKey = moment().utc().startOf("day").format("YYYY-MM-DD")
    // query the table
    query(process.env.EVENT_TABLE_NAME, groupingKey).then(data => {
        //return the data array
        return callback(null, {
            "isBase64Encoded": false,
            "statusCode": 200,
            "headers": { 
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
             },
            "body": JSON.stringify(data)
        });
    }).catch(err => {
        console.log(err)
        return callback(null, {
            "isBase64Encoded": false,
            "statusCode": 500,
            "headers": { 
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
             },
            "body": JSON.stringify(err)
        });
    })
    
};