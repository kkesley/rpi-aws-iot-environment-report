# Simple Realtime Environment Reporting using AWS IOT & Raspberry Pi

Realtime Temperature / Humidity / Pressure reporting using raspberry pi and AWS IoT

## Prerequisite

1. NodeJS: https://nodejs.org/en/

1. Python 3.5+: https://www.python.org/downloads/

## Front End

Run `npm install` in the `front-end` folder

Create `AppSync.js` in `front-end/src/Config`. Use the template provided `AppSync.tmpl.js`. Don't forget to change the variables.

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


Create `serverless.yml` in `./server`. Use the template provided `serverless.tmpl.yml`. Don't forget to change the custom variables.

Deploy the application using `sls deploy`

1. Go to AWS AppSync, create a project and start with the schema in `schema.graphql` placed in this repo.

1. Connect the mutation and query with the dynamodb table which is created later by the serverless framework


## Raspberry PI

Designed using `Raspberry Pi 3 model B` & `Raspberry Pi sense hat`. Make sure you install the prerequisites in your raspberry pi.

### Prerequisite

1. pip

1. `pip install influxdb`

1. start influxdb `sudo service influxdb start` or you can make it auto start on reboot using `sudo update-rc.d influxdb defaults`

1. Create influxdb user and database. you can go to the admin page at `{your raspberry ip address}:8083`. Note that the port may not always be `8083`. Please check if you cannot use port `8083`

1. `pip install AWSIoTMQTTClient`

1. `pip install SenseHat`

1. Create your device in AWS IoT Core. use this guide https://docs.aws.amazon.com/iot/latest/developerguide/iot-sdk-setup.html

1. Make note of your certificate location. Will be used in `config` file (`aws-iot.json`)

Create `aws-iot.json` in `./raspberry-pi/config`. Use the template provided `aws-iot.tmpl.json`. Don't forget to change the variables.

Create `pushbullet.json` in `./raspberry-pi/config`. Use the template provided `pushbullet.tmpl.json`. Don't forget to change the variables.

Create `influxdb.json` in `./raspberry-pi/config`. Use the template provided `influxdb.tmpl.json`. Don't forget to change the variables.
