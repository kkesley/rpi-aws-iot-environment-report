const AWS = require('aws-sdk')
const update = (table = "", key = "", {timestamp, temperature, humidity, deviceid} = {}) => {
    return new Promise((res, rej) => {
        var docClient = new AWS.DynamoDB.DocumentClient()
        var params = {
            TableName:table,
            Key:{
                "groupingKey": key,
                "timestamp": 0,
            },
            UpdateExpression: "set #temp = :temp, #hum = :hum, #device = :device",
            ExpressionAttributeNames: {
                "#temp": "temperature",
                "#hum": "humidity",
                "#device": "device",
            },
            ExpressionAttributeValues:{
                ":hum": humidity,
                ":temp": temperature,
                ":device":deviceid,
            },
            ReturnValues:"UPDATED_NEW"
        };

        console.log("Updating the item...");
        docClient.update(params, function(err, data) {
            if (err) {
                console.error("Unable to update item. Error JSON:", JSON.stringify(err, null, 2));
                rej()
            } else {
                console.log("UpdateItem succeeded:", JSON.stringify(data, null, 2));
                res()
            }
        });
    })
}

module.exports = update