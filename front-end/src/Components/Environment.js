import React, { Component } from 'react';
import { graphql, compose } from 'react-apollo';
import GetEnvironment from '../Graphql/Queries/GetEnvironment'
import SubscribeEnvironment from '../Graphql/Subscription/SubscribeEnvironment'
import quotes from './quotes'
import { LineChart, Line, ResponsiveContainer, Tooltip, CartesianGrid, XAxis, YAxis } from 'recharts';



class Environment extends Component {
    componentWillMount(){
      this.props.environmentSubscription();
    }
    getColor(temperature){
        if(temperature > 30){
            return "#b90b0b"
        }else if (temperature > 10){
            return "#2bbb4b"
        }else{
            return "#3557ff"
        }
    }
    getBackground(temperature){
        if(temperature > 30){
            return "url(./temp-hot.jpg)"
        }else if (temperature > 10){
            return "url(./temp-medium.jpg)"
        }else{
            return "url(./temp-cold.jpg)"
        }
    }
    getQuote(temperature){
        var tempQuotes = []
        if(temperature > 30){
            tempQuotes = quotes.hot
        }else if (temperature > 10){
            tempQuotes = quotes.medium
        }else{
            tempQuotes = quotes.cold
        }
        return tempQuotes[Math.floor(Math.random()*tempQuotes.length)]
    }
    render(){
      console.log(this.props)
      const color = this.getColor(this.props.environment.temperature)
      const quote = this.getQuote(this.props.environment.temperature)
      const data = [
        {name: 'Page A', temp: 4000},
        {name: 'Page B', temp: 3000},
        {name: 'Page C', temp: 2000},
        {name: 'Page D', temp: 2780},
        {name: 'Page E', temp: 1890},
        {name: 'Page F', temp: 2390},
        {name: 'Page G', temp: 3490},
      ]
      return (
        <div className="m-grid__item m-grid__item--fluid m-grid  m-error-3" style={{backgroundImage: this.getBackground(this.props.environment.temperature)}}>
          <div className="m-error_container">
            <span className="m-error_number">
              <h1 style={{color: color, textStrokeColor: color, WebkitTextStrokeColor: color}}>
              {this.props.environment.temperature} <sup style={{marginLeft:-30,fontSize: '6rem'}}>&deg;C</sup>
              </h1>
            </span>
            <div className="m-error_description">
                <blockquote>
                {quote.text}
                </blockquote>
                <cite>– {quote.cite}</cite>
            </div>
          </div>
          <div style={{height: 300, width:"50%", marginLeft: 20, backgroundColor:"#FFFFFF"}}>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={data}>
                <XAxis dataKey="name" />
                <YAxis />
                <CartesianGrid strokeDasharray="3 3" />
                <Tooltip />
                <Line type="monotone" dataKey="temp" stroke="#8884d8" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      )
    }
  }
  
export default compose(
    graphql(GetEnvironment, {
        options: {
            fetchPolicy: 'cache-and-network',
            variables: {
              groupingKey: "now",
              timestamp: 0
            },
        },
        props: (props) => ({
            environment: props.data.getEnvironment,
            environmentSubscription: params => {
              props.data.subscribeToMore({
                  variables: {
                    groupingKey: "now",
                    timestamp: 0
                  },
                  document: SubscribeEnvironment,
                  updateQuery: (prev, { subscriptionData: { data : { onCreateEnvironment } } }) => ({
                    ...prev,
                    getEnvironment: {...onCreateEnvironment }
                  })
              });
          },
        })
    }),
    )(Environment);