const AWS = require('aws-sdk')
const moment = require('moment')
module.exports = (table, key) => {
    return new Promise((res, rej) => {
        var docClient = new AWS.DynamoDB.DocumentClient()
        var params = {
            TableName: table,
            ProjectionExpression: "created_at, temperature, pressure, humidity, device",
            KeyConditionExpression: "#key = :key and #timestamp < :timestamp",
            ExpressionAttributeNames: {
                "#key": "groupingKey",
                "#timestamp": "timestamp",
            },
            ExpressionAttributeValues:{
                ":key": key,
                ":timestamp": moment().utc().valueOf(),
            },
            Limit: 20,
        };

        console.log("querying items...");
        docClient.query(params, function(err, data) {
            if (err) {
                console.error("Unable to query item. Error JSON:", JSON.stringify(err, null, 2));
                rej(err)
            } else {
                console.log("Query succeeded:", JSON.stringify(data, null, 2));
                res(data)
            }
        });
    })
}