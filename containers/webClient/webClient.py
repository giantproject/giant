import os
from flask import Flask, redirect, url_for, render_template, request
import json
import requests
import json

app = Flask(__name__)
ipInfoIp = os.environ['IPINFO_1_PORT_5002_TCP_ADDR']
pyWhoIsIp = os.environ['PYWHOIS_1_PORT_5001_TCP_ADDR']
eventIp = os.environ['EVENT_1_PORT_5000_TCP_ADDR']

@app.route('/')
@app.route('/home.html')
def home():
    
    return render_template("home.html")

@app.route('/displayip.html')
def displayip():
    unparsed_json = ()
    return render_template("displayip.html", parsed_json = unparsed_json);

@app.route('/displaydomain.html')
def displaydomain():
    unparsed_json = ()
    return render_template("displaydomain.html", parsed_json = unparsed_json)

@app.route('/displayevent.html')
def displayevent():
    unparsed_json = ()
    return render_template("displayevent.html", parsed_json = unparsed_json)

@app.route('/ipinfo', methods=['POST'])
def ipInfo():
    ip = request.form['ip']
    unparsed_json = requests.get('http://'+ipInfoIp+':5002/ipinfo/'+ip).text
    return render_template('displayip.html', parsed_json = unparsed_json)
	
@app.route('/pywhois', methods=['POST'])
def pyWhoIs():
    domain = request.form['domain']
    unparsed_json = requests.get('http://'+pyWhoIsIp+':5001/pywhois/'+domain).text
    return render_template('displaydomain.html', parsed_json = unparsed_json)

@app.route('/event', methods=['POST'])
def event():
    name = request.form['name']
    description = request.form['description']
    comments = request.form['comments']
    requests.post('http://'+eventIp+':5000/event/', request.form)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5003, debug=True)
