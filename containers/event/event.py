import os
from flask import Flask, redirect, url_for, render_template, request
import json
import whois
import requests

app = Flask(__name__)



@app.route('/')
def help():
    help = "Format for accessing. 'https://ipAddress/pywhois/domain' But anyway You made it here"
    return help
@app.route('/event', methods=['POST'])
def event():
    event = {}
    event['name'] = request.form['name']
    event['description'] = request.form['description']
    event['AnalystComments'] = request.form['AnalystComments']
    return json.dumps(event)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

