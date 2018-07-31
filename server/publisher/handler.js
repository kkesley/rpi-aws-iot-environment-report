const AWS = require('aws-sdk')
const config = require('./config').default;
const axios = require('axios')
module.exports.main = (event, context, callback) => {
    if(!event.temperature || !event.humidity || !event.deviceid || !event.timestamp || !event.pressure){
        return callback(null, "invalid request");
    }
    publish(event).then(result => {
        console.log(result.data)
        console.log(result.data.errors)
        return callback(null, "Success publishing")
    }).catch(err => {
        return callback(null, "Error publishing")
    })
};

function publish(event){
    // Require exports file with endpoint and auth info
    
    let req = new AWS.HttpRequest(config.ENDPOINT, config.REGION);
    req.method = 'POST';
    req.headers.host = config.HOST;
    req.headers['Content-Type'] = 'multipart/form-data';
    req.headers["x-api-key"] = process.env.APPSYNC_API_KEY
    req.body = JSON.stringify({
        // "query":"mutation ($input: UpdateUsersCamsInput!) { updateUsersCams(input: $input){ latestImage uid name } }",
        query: "mutation ($input: CreateEnvironmentInput!) {createEnvironment(input: $input){groupingKey timestamp temperature humidity pressure device created_at } }",
        variables: {
            input: {
                groupingKey: "now",
                timestamp: 0,
                temperature: event.temperature,
                humidity: event.humidity,
                pressure: event.pressure,
                device: event.deviceid,
                created_at: event.timestamp,
            }
        }
    });

    return axios({
        method: 'post',
        url: config.ENDPOINT,
        data: req.body,
        headers: req.headers
    });
}