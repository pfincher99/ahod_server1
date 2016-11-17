# All Hands On Deck IoT Demo - Web Service
## This repo is used as part of the IMAPEX "All Hands On Deck" IoT demo.

The full description of the demo can be found here:
* https://github.com/pfincher99/ahod_home

This application has the following functions:
* Web Service [API](https://github.com/pfincher99/ahod_webapp/blob/master/API.md) for the IoT device sending PLC data.
* Initiates API calls to Cisco Spark to post the information received from the IoT device

This application can be deployed to the Marathon container that was deployed via the Web Service Container scripts:
* https://github.com/pfincher99/ahod_websvc
