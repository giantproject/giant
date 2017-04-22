import os
from flask import Flask, redirect, url_for, render_template, request
import json
import requests
from pymongo import MongoClient
import datetime
from bson import json_util

app = Flask(__name__)

client = MongoClient(os.environ['DB_1_PORT_27017_TCP_ADDR'], 27017)
db= client.db
invalidString = "Please provide a valid IP address"
@app.route('/')
def help():
    help = "Format for accessing. 'https://ipAddress/ipinfo/url_to_search' But anyway You made it here"
    return help
@app.route('/ipinfo')
@app.route('/ipinfo/<ip>')
def ipinfo(ip=''):
    findResult = findRecord(ip)
    if (findResult is not None):
    	id = findResult.get('_id')t 
        return json_util.dumps({"status":"Found", "id": str(id), "result": findResult})
    lookup = "http://ipinfo.io/" + ip
    result = requests.get(lookup)
    if (result.text == invalidString):
        return "{\"status\": \"Failure\", \"error\": {}}",format(invalidString)
    result = json.loads(result.text)
    result['time'] = datetime.datetime.now()
    insertionResult = insertRecord(result)
    if (insertionResult['status'] != "Success"):
        return insertionResult
    insertionResult['result'] = result
    return json_util.dumps(insertionResult)

def insertRecord(record):
    try:
        id = db.ipinfo.insert_one(record).inserted_id
        return {"status":"Success", "id":str(id)}
    except Exception as e:
        return {"status":"Failure", "error": str(e)}

def findRecord(ip):
    try:
        record = db.ipinfo.find_one({'ip':ip})
        if (record is not None):
            return record
        else:
            return None
    except:
        return None

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

