const AWS = require('aws-sdk')
const update = (table = "", key = "", time = 0, {timestamp, temperature, humidity, deviceid, pressure} = {}) => {
    return new Promise((res, rej) => {
        var docClient = new AWS.DynamoDB.DocumentClient()
        var params = {
            TableName:table,
            Key:{
                "groupingKey": key,
                "timestamp": time,
            },
            UpdateExpression: "set #temp = :temp, #hum = :hum, #device = :device, #ca = :ca, #pres = :pres",
            ExpressionAttributeNames: {
                "#temp": "temperature",
                "#hum": "humidity",
                "#device": "device",
                "#ca": "created_at",
                "#pres": "pressure"
            },
            ExpressionAttributeValues:{
                ":hum": humidity,
                ":temp": temperature,
                ":device":deviceid,
                ":ca": timestamp,
                ":pres": pressure
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