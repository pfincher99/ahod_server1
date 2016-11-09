from flask import Flask, request
from flask_restful import Resource, Api, reqparse
## testing branch to dev

app = Flask(__name__)
app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        text = "Hello World! Im working"
        return text

api.add_resource(HelloWorld, '/hello/world')

class Alert(Resource):
    def get(self):
        text = "Alert Received"
        return text

api.add_resource(Alert, '/alert')

if __name__ == '__main__':
    # Run Flask
    app.run(debug=True, host='0.0.0.0', port=int("5000"))

# adding code to test dev branch deployment
# more and more