import os
from flask import Flask, redirect, url_for, render_template, request
import json
import whois
import requests
from pymongo import MongoClient
from bson import json_util
app = Flask(__name__)

client = MongoClient(os.environ['DB_1_PORT_27017_TCP_ADDR'], 27017)
db = client.db

@app.route('/')
def help():
    help = "Format for accessing. 'https://ipAddress/pywhois/domain' But anyway You made it here"
    return help
@app.route('/pywhois/<domain>')
def pywhois(domain):
    findResult = findRecord(domain)
    if (findResult is not None):
        id = findResult.get('_id')
        return json_util.dumps({"status":"Found", "id": str(id), "result": findResult})
    try:
        w = whois.whois(domain)
    except Exception as e:
        return json.dumps({"status":"Failure", "error":str(e)})
    w = json.loads(str(w))
    insertionResult=insertRecord(w, domain)
    if (insertionResult['status'] != "Success"):
        return json_util.dumps(insertionResult)
    insertionResult['result'] = w
    return json_util.dumps(insertionResult)

def insertRecord(record, domain):
    try:
        record['search_domain'] = domain
        id = db.pywhois.insert_one(record).inserted_id
        return {"status":"Success", "id":str(id)}
    except Exception as e:
        return {"status":"Failure", "error":str(e)}


def findRecord(domain):
    try:
        record = db.pywhois.find_one({'search_domain':domain})
        if (record is not None):
            return record
        else:
            return None
    except:
        return None


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)

