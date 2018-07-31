const moment = require('moment-timezone')
const query = require('./query')
module.exports.main = (event, context, callback) => {
    var groupingKey = moment().utc().startOf("day").format("YYYY-MM-DD")
    query(process.env.EVENT_TABLE_NAME, groupingKey).then(data => {
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