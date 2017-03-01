import os
from flask import Flask, redirect, url_for, render_template, request
import json
import requests

app = Flask(__name__)



@app.route('/')
def help():
    help = "Format for accessing. 'https://ipAddress/ipinfo/url_to_search' But anyway You made it here"
    return help
@app.route('/ipinfo')
@app.route('/ipinfo/<ip>')
def ipinfo(ip=''):
    lookup = "http://ipinfo.io/" + ip
    result = requests.get(lookup)
    return result.text

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

