var config = {
    HOST: process.env.APPSYNC_HOST,
    REGION: process.env.APPSYNC_REGION,
    PATH: '/graphql',
    ENDPOINT: '',
};
config.ENDPOINT = "https://" + config.HOST + config.PATH;
exports.default = config;