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
@app.route('/pywhois/<domain>')
def pywhois(domain):
    w = whois.whois(domain)
    w = str(w)
    return w   

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001 debug=True)

