##
import sqlite3
import os
import json
import requests

from flask import Flask, request, jsonify
from flask_restful import Resource, Api

db_loc = "ahod.db"

# Spark information
room_url = 'https://api.ciscospark.com/v1/messages'
room_id = os.environ['SPARK_ROOM']
spark_token = "Bearer " + os.environ['SPARK_TOKEN']


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


## Flask Server
app = Flask(__name__)
api = Api(app)


# Start: Hello world code not used for API only for testing at this stage
class HelloWorld(Resource):
    def get(self):
        text = "Hello World! This is the dev branch"
        return text


api.add_resource(HelloWorld, '/hello/world')


class Alert(Resource):
    def get(self):
        text = "Alert Received"
        return text


api.add_resource(Alert, '/alert')


# End: Hello world code not used for API only for testing at this stage

# API code for ahod web server
@app.route("/ahod", methods=['GET'])
def validate():
    # return jsonify({"version":"1.0 ","switchName":"info0","message":"info1","plcInfo":{"plcName":"info2","plcDataPoint":"info3","plcLocation":"info4","plcIp":"info5"}})
    conn = sqlite3.connect(db_loc)
    cur = conn.cursor()
    cur.execute('''SELECT switchName, message, plcName, plcDataPoint, plcLocation, plcIp FROM Devices''')
    result = cur.fetchall()

    for response in result:
        switchName = response[0]
        switchName = str(switchName)
        message = response[1]
        message = str(message)
        plcName = response[2]
        plcName = str(plcName)
        plcDataPoint = response[3]
        plcDataPoint = str(plcDataPoint)
        plcLocation = response[4]
        plcLocation = str(plcLocation)
        plcIp = response[5]
        plcIp = str(plcIp)
        return jsonify({"version": "1.0 ", "switchName": switchName, "message": message,
                        "plcInfo": {"plcName": plcName, "plcDataPoint": plcDataPoint, "plcLocation": plcLocation,
                                    "plcIp": plcIp}})
    cur.close()


@app.route("/ahod", methods=['POST'])
def receiver():
    global post_data
    create_db()
    post_data = request.get_data()
    plc_data()
    post_spark()
    return jsonify(result={"status": 200})


def post_spark():
    global room_url, switchName, message, plcName, plcDataPoint, plcLocation, plcIp
    print "post data to Spark"
    print room_id
    print spark_token
    headers = {'content-type': 'application/json', 'Authorization': spark_token}
    #data = "test from flask server"
    data = "**Switch:** " + switchName + "\n- **PLC:** " + plcName + "\n- **PLC Data Point:** " + plcDataPoint + "\n- **PLC Location:** " + plcLocation + "\n- **PLC IP Address:** " + plcIp + "\n- **Message:** " + message
    payload_json1 = {
        "roomId": room_id,
        "markdown": data
    }
    print payload_json1
    requests.post(room_url, headers=headers, data=json.dumps(payload_json1))
    # conv_response_json = spark_post.json()
    # print conv_response_json


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
        INSERT INTO devices
        (switchName, message, plcName, plcDataPoint, plcLocation, plcIp )
        VALUES (?, ?, ?, ?, ?, ? )''', (switchName, message, plcName, plcDataPoint, plcLocation, plcIp))
    conn.commit()
    print "wrote data to DB"


if __name__ == '__main__':
    port = 5000  # the custom port you want
    app.run(host='0.0.0.0', port=port)
    app.debug = True
