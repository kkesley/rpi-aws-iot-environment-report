const AWS = require('aws-sdk')
const config = require('./config').default; // Require config file with endpoint and auth info
const axios = require('axios')
module.exports.main = (event, context, callback) => {
    //required fields
    if((!event.temperature && event.temperature !== 0) || (!event.humidity && event.humidity !== 0) || !event.deviceid || !event.timestamp || (!event.pressure && event.pressure !== 0)){
        return callback(null, "invalid request");
    }
    //publish the event to app sync
    publish(event).then(result => {
        console.log(result.data)
        console.log(result.data.errors)
        return callback(null, "Success publishing")
    }).catch(err => {
        return callback(null, "Error publishing")
    })
};

function publish(event){
    // construct request object
    let req = new AWS.HttpRequest(config.ENDPOINT, config.REGION);
    req.method = 'POST';
    req.headers.host = config.HOST; // app sync host
    req.headers['Content-Type'] = 'multipart/form-data';
    req.headers["x-api-key"] = process.env.APPSYNC_API_KEY // app sync key
    req.body = JSON.stringify({
        query: "mutation ($input: CreateEnvironmentInput!) {createEnvironment(input: $input){groupingKey timestamp temperature humidity pressure device created_at } }", //graphql query for publishing
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

    // fire the request!
    return axios({
        method: 'post',
        url: config.ENDPOINT,
        data: req.body,
        headers: req.headers
    });
}