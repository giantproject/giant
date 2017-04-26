import os
from flask import Flask, redirect, url_for, render_template, request
import json
import requests
import json

app = Flask(__name__)
ipInfoIp = os.environ['IPINFO_1_PORT_5000_TCP_ADDR']
pyWhoIsIp = os.environ['PYWHOIS_1_PORT_5000_TCP_ADDR']
eventIp = os.environ['EVENT_1_PORT_5000_TCP_ADDR']
whatIsIp = os.environ['WHATIS_1_PORT_5000_TCP_ADDR']


@app.route('/')
@app.route('/home.html')
def home():
    # return json.dumps({"vars":str(os.environ)})
    return render_template("home.html")


@app.route('/displayip.html')
def displayip():
    unparsed_json = ()
    return render_template("displayip.html", parsed_json=unparsed_json);


@app.route('/displaydomain.html')
def displaydomain():
    unparsed_json = ()
    return render_template("displaydomain.html", parsed_json=unparsed_json)


@app.route('/displayevent.html')
def displayevent():
    unparsed_json = ()
    return render_template("displayevent.html", parsed_json=unparsed_json)


@app.route('/displaywhatis.html')
def displaywhatis():
    unparsed_json = ()
    return render_template("displaywhatis.html", parsed_json=unparsed_json)


@app.route('/getiptable', methods=['POST'])
def getIpTable():
    unparsed_json = requests.get('http://'+ipInfoIp+':5000/ipinfo/table').text
    return unparsed_json


@app.route('/getdomaintable', methods=['POST'])
def getDomainTable():
    unparsed_json = requests.get('http://' + pyWhoIsIp + ':5000/pywhois/table').text
    return unparsed_json


@app.route('/ipinfo', methods=['POST'])
def ipInfo():
    ip = request.form['ip']
    unparsed_json = requests.get('http://'+ipInfoIp+':5000/ipinfo/'+ip).text
    return render_template('displayip.html', parsed_json = unparsed_json)

@app.route("/ipinfo/cli", methods=['POST'])
def ipInfoCLI():
    ip = request.form['ip']
    return requests.get('http://' + ipInfoIp + ':5000/ipinfo/' + ip).text


@app.route('/pywhois', methods=['POST'])
def pyWhoIs():
    domain = request.form['domain']
    unparsed_json = requests.get('http://' + pyWhoIsIp + ':5000/pywhois/' + domain).text
    return render_template('displaydomain.html', parsed_json=unparsed_json)


@app.route('/pywhois/cli', methods=['POST'])
def pyWhoIsCLI():
    domain = request.form['domain']
    return requests.get('http://'+pyWhoIsIp+':5000/pywhois/'+domain).text

@app.route('/event', methods=['POST'])
@app.route('/event/cli',methods=['POST']) # Makes it easier for the CLI to work
def event():
    r = requests.post('http://' + eventIp + ':5000/event', request.form)
    if r.status_code == 200:
        return r.text
    return request.form


@app.route('/whatis', methods=['POST'])
def whatIs():
    portNum = request.form['number']
    proto = request.form['proto']
    unparsed_json = requests.get('http://' + whatIsIp + ':5000/whatis/' + portNum + '/' + proto).text
    return render_template('displaywhatis.html', parsed_json=unparsed_json)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
