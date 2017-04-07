import os
from flask import Flask, redirect, url_for, render_template, request
import json
import requests

app = Flask(__name__)
ipInfoIp = os.environ['TODO_CONTAINERS_IPINFO_1_PORT_5002_TCP_ADDR']

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/ipinfo', methods=['POST'])
def ipInfo():
    ip = request.form['ip']
    return request.get(ipInfoIp+':5002/ipinfo/'+ip)
	


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5003, debug=True)
