import sqlite3
import os
import json

from flask import Flask, request, jsonify
from flask_restful import Resource, Api

db_loc = "/ahod.db"


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
    return "RESPONSE TO GET"


@app.route("/ahod", methods=['POST'])
def receiver():
    global post_data
    create_db()
    post_data = request.get_data()
    parse_all()
    return jsonify(result={"status": 200})


def parse_all():
    global post_data
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

    switchName = ['switchName']
    message = ['message']
    plcName = ['plcInfo']['plcName']
    plcDataPoint = ['plcInfo']['plcDataPoint']
    plcLocation = ['plcInfo']['plcLocation']
    plcIp = ['plcInfo']['plcIp']
    cur.execute('''
        INSERT INTO devices
        (switchName, message, plcName, plcDataPoint, plcLocation, plcIp )
        VALUES (?, ?, ?, ?, ?, ? )''', (switchName, message, plcName, plcDataPoint, plcLocation, plcIp))
    conn.commit()


if __name__ == '__main__':
    port = 5000  # the custom port you want
    app.run(host='0.0.0.0', port=port)