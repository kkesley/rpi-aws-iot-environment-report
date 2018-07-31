import React, { Component } from 'react';
import './App.css';
import { ApolloProvider } from 'react-apollo';
import { Rehydrated } from 'aws-appsync-react';

import client from './AppSync'
import EnvironmentContainer from './Components/Environment'
class App extends Component {
  render() {
    return (
      <div className="m-grid m-grid--hor m-grid--root m-page">
        <EnvironmentContainer/>
      </div>
      
    );
  }
}

const WithProvider = () => (
  <ApolloProvider client={client}>
      <Rehydrated className="asd">
          <App />
      </Rehydrated>
  </ApolloProvider>
);

export default WithProvider;


