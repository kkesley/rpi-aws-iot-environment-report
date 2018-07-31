import gql from 'graphql-tag';

export default gql`
query GetEnvironment($groupingKey: ID!, $timestamp: Int!) {
    getEnvironment(groupingKey: $groupingKey, timestamp: $timestamp){
      groupingKey
      timestamp
      temperature
      pressure
      humidity
      device
      created_at
    }
}`;