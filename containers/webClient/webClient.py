import os
from flask import Flask, redirect, url_for, render_template, request
import json
import requests

app = Flask(__name__)


@app.route('/')
def home():
    return "hello"




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5003, debug=True)
