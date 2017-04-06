import os
from flask import Flask, redirect, url_for, render_template, request
import json
import requests

app = Flask(__name__)

'''client = MongoClient(os.environ['DB_1_PORT_27017_TCP_ADDR'], 27017)'''
'''db= client.db'''

ipInfoURL = os.environ['IPINFO_1_PORT_5002_TCP_ADDR']


@app.route('/')
def home():
    return "hello"


# ipinfoURL = os.environ['IPINFO_1_PORT_5002_TCP_ADDR']
# render_template('home.html')

@app.route('/ipinfo')
def ipinfo():
    ip = request.args.get('ip')
    r = requests.get(ipInfoURL + '/ipinfo/' + ip)
    return r.json()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5003, debug=True)