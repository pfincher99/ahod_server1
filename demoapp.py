##
import sqlite3
import os
import json
import requests

from flask import Flask, request, jsonify
from flask_restful import Resource, Api


# Information required for Spark
room_url = 'https://api.ciscospark.com/v1/messages'
room_id = os.getenv("spark_room")
token = os.getenv("spark_token")
spark_token = "Bearer "+str(token)


#SQLite3 database for storing PLC data posted from the IE4000
db_loc = "ahod.db"
def create_db():
    global conn, cur
    # check to see if db exists, if not, create
    if os.path.exists(db_loc):
        print("DB Exists")
        print ""
    else:
        conn = sqlite3.connect(db_loc)
        cur = conn.cursor()
        cur.execute('''
        CREATE TABLE Devices (
            id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            switchName	TEXT,
            message		TEXT,
            plcName		TEXT,
            plcDataPoint	TEXT,
            plcLocation	TEXT,
            plcIp		TEXT
        )
        ''')
        cur.close()


## Flask Web Server
app = Flask(__name__)
api = Api(app)


# Start: This code not used for API only for testing at this stage
class HelloWorld(Resource):
    def get(self):
        text = "Hello World! This is the Master branch"
        return text
api.add_resource(HelloWorld, '/hello/world')


class Alert(Resource):
    def get(self):
        text = "Alert Received on Master Branch"
        return text
api.add_resource(Alert, '/alert')
# End: code not used for API only for testing at this stage


# Handler to respond to a GET request for the latest posted PLC data
@app.route("/ahod", methods=['GET'])
def validate():
    conn = sqlite3.connect(db_loc)
    cur = conn.cursor()
    cur.execute('''SELECT * FROM Devices ORDER BY id DESC''') #DESC Orders by latest first

    for response in cur:
        switchName = response[1]
        switchName = str(switchName)
        message = response[2]
        message = str(message)
        plcName = response[3]
        plcName = str(plcName)
        plcDataPoint = response[4]
        plcDataPoint = str(plcDataPoint)
        plcLocation = response[5]
        plcLocation = str(plcLocation)
        plcIp = response[6]
        plcIp = str(plcIp)
        return jsonify({"version": "1.0 ", "switchName": switchName, "message": message,
                        "plcInfo": {"plcName": plcName, "plcDataPoint": plcDataPoint, "plcLocation": plcLocation,
                                    "plcIp": plcIp}})
    cur.close()

# Handler to receive PLC data posted from the IE4000 application
@app.route("/ahod", methods=['POST'])
def receiver():
    global post_data
    create_db()
    post_data = request.get_data()
    plc_data()
    get_sip_uri()
    post_spark()
    return jsonify(result={"status": 200})

# Function to enter the PLC data received from the IE4000 POST to the SQL database
def plc_data():
    global post_data, switchName, message, plcName, plcDataPoint, plcLocation, plcIp
    conn = sqlite3.connect(db_loc)
    cur = conn.cursor()
    info = json.loads(post_data)
    print info['version']
    print info['switchName']
    print info['message']
    print info['plcInfo']['plcName']
    print info['plcInfo']['plcDataPoint']
    print info['plcInfo']['plcLocation']
    print info['plcInfo']['plcIp']
    switchName = info['switchName']
    message = info['message']
    plcName = info['plcInfo']['plcName']
    plcDataPoint = info['plcInfo']['plcDataPoint']
    plcLocation = info['plcInfo']['plcLocation']
    plcIp = info['plcInfo']['plcIp']
    cur.execute('''
        INSERT INTO Devices
        (switchName, message, plcName, plcDataPoint, plcLocation, plcIp )
        VALUES (?, ?, ?, ?, ?, ? )''', (switchName, message, plcName, plcDataPoint, plcLocation, plcIp))
    conn.commit()
    print "wrote data to DB"

# Function to get the SIP URI of the Spark Room (future use case)
@app.route("/uri", methods=['GET'])
def get_sip_uri():
    global room_id, spark_token, sip_addr
    get_room_url = 'https://api.ciscospark.com/v1/rooms/' + str(room_id)
    headers = {'content-type':'application/json','Authorization': spark_token}
    payload = {'showSipAddress': 'true'}
    spark_post = requests.get(get_room_url, headers=headers, params=payload)
    conv_response_json = spark_post.json()
    sip_addr = conv_response_json[u'sipAddress']
    return sip_addr

# Function to post the latest received PLC data to Spark from the SQL database
def post_spark():
    global room_url, switchName, message, plcName, plcDataPoint, plcLocation, plcIp
    print "post data to Spark"
    print room_id
    print spark_token
    headers = {'content-type': 'application/json', 'Authorization': spark_token}
    data = "**Switch:** " + switchName + "\n- **PLC:** " + plcName + "\n- **PLC Data Point:** " + plcDataPoint + "\n- **PLC Location:** " + plcLocation + "\n- **PLC IP Address:** " + plcIp + "\n- **Message:** " + message
    payload_json1 = {
        "roomId": room_id,
        "markdown": data
    }
    print payload_json1
    requests.post(room_url, headers=headers, data=json.dumps(payload_json1))


if __name__ == '__main__':
    port = 5000  # the custom port you want
    app.run(host='0.0.0.0', port=port)
    app.debug = True
