import gql from 'graphql-tag';

export default gql`
subscription SubscribeEnvironment($groupingKey: ID!, $timestamp: Int!){
    onCreateEnvironment(groupingKey: $groupingKey, timestamp: $timestamp){
      groupingKey
      timestamp
      temperature
      humidity
      device
      created_at
    }
}`;