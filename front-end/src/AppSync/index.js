import { AUTH_TYPE } from "aws-appsync/lib/link/auth-link";
import AppSync from '../Config/AppSync'
import AWSAppSyncClient from "aws-appsync";
export default new AWSAppSyncClient({
    url: AppSync.graphqlEndpoint,
    region: AppSync.region,
    auth: {
        type: AUTH_TYPE.API_KEY,
        apiKey: AppSync.apiKey,
    },
});