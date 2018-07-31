# Raspberry Pi Environment Reporting using AWS IOT

Realtime Temperature / Humidity / Pressure reporting using raspberry pi and AWS IoT

## Prerequisite

1. NodeJS: https://nodejs.org/en/

1. Python 3.5+: https://www.python.org/downloads/

## Front End

Run `npm install` in the `front-end` folder

Try the app using `npm run start` / `yarn start`


## Server

This application is designed to use AWS Services.

- DynamoDB
- AppSync
- Lambda
- Api Gateway
- IoT

Note: the application is designed to stay within free tier limitation. If your free tier has expired / you have more services running in your AWS account, you may pay for running this application.

### Prerequisite

1. Serverless: `npm i -g serverless`

1. AWS Account

1. AWS CLI https://docs.aws.amazon.com/cli/latest/userguide/installing.html

1. AWS Credentials attached in the computer https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html

Deploy the application using `sls deploy`


## Raspberry PI

Designed using `Raspberry Pi 3 model B` & `Raspberry Pi sense hat`. Make sure you install the prerequisites in your raspberry pi.

### Prerequisite

1. pip

1. `pip install AWSIoTMQTTClient`

1. `pip install SenseHat`
