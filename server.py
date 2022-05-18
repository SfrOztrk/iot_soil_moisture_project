"""
A HTTP RESTFul API server to control the water pump built using Flask-RESTful.

Dependencies:
  pip3 install gpiozero pigpio flask-restful

"""

import RPi.GPIO as GPIO
import time
import logging
from flask import Flask, request, render_template
from flask_restful import Resource, Api, reqparse, inputs



# Global variables
WATER_PUMP = 7
#HUMIDITY_SENSOR = 40
#MOISTURE_SENSOR = 11
state = {
    'level': 0 	# state of the water pump.
}

GPIO.setmode(GPIO.BOARD)
GPIO.setup(WATER_PUMP, GPIO.OUT)
#GPIO.setup(humidity_sensor, GPIO.IN)



# Flask & Flask-RESTful instance variables
app = Flask(__name__) # Core Flask app.
api = Api(app) # Flask-RESTful extension wrapper



# @app.route applies to the core Flask instance (app).
# Here we are serving a simple web page.
@app.route('/', methods=['GET'])
def index():
    """Make sure inde.html is in the templates folder
    relative to this Python file."""
    return render_template('index_api_client.html', pin=WATER_PUMP)



# Flask-restful resource definitions.
# A 'resource' is modeled as a Python Class.
class PumpControl(Resource):  # (10)

    def __init__(self):
        self.args_parser = reqparse.RequestParser()

        self.args_parser.add_argument(
            name='level',	# Name of arguement
            required=True,  	# Mandatory arguement
            type=inputs.int_range(0, 1),	# Allowed 0 or 1
            help='Set level of the water pump {error_msg}',
            default=None)


    def get(self):
        """ Handles HTTP GET requests to return current water pump level."""
        return state


    def post(self):
        """Handles HTTP POST requests to set water pump level."""
        global state

        args = self.args_parser.parse_args()

        state['level'] = args.level
        GPIO.output(WATER_PUMP, state['level'])
        return state


# Register Flask-RESTful resource and mount to server end point /led
api.add_resource(PumpControl, '/pump')


if __name__ == '__main__':

    # If you have debug=True and receive the error "OSError: [Errno 8] Exec format error", then:
    # remove the execuition bit on this file from a Terminal, ie:
    # chmod -x flask_api_server.py
    #
    # Flask GitHub Issue: https://github.com/pallets/flask/issues/3189

    app.run(host="0.0.0.0", debug=True)
