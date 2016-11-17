# All Hands On Deck IoT Demo - API

### POST

`http://imapex-ahod-ahod-server.green.browndogtech.com/ahod`

### HEADERS
**Content-Type**        application/json

### BODY
`
{
  "message": "string",
  "plcInfo": {
    "plcDataPoint": "string",
    "plcIp": "string",
    "plcLocation": "string",
    "plcName": "string"
  },
  "switchName": "string",
  "version": "1.0 "
}
`