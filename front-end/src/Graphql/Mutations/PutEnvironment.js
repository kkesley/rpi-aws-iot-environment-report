import gql from 'graphql-tag';

export default gql`
mutation PutEnvironment($input: CreateEnvironmentInput!) {
    createEnvironment(input: $input){
      groupingKey
      timestamp
      temperature
      humidity
      device
      created_at
    }
}`;