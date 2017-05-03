import os
from flask import Flask, redirect, url_for, render_template, request
import json
import whois
from datetime import datetime
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
    w["time"] = str(datetime.now())
    insertionResult=insertRecord(w, domain)
    if (insertionResult['status'] != "Success"):
        return json_util.dumps(insertionResult)
    insertionResult['result'] = w
    return json_util.dumps(insertionResult)

def insertRecord(record, domain):
    try:
        record['search_domain'] = domain
        db.pywhois.insert_one(record)
        return {"status":"Success" }
    except Exception as e:
        return {"status":"Failure", "error":str(e)}


def findRecord(domain):
    try:
        record = db.pywhois.find_one({'search_domain':domain}, {"_id":False})
        if (record is not None):
            return record
        else:
            return None
    except:
        return None

@app.route("/pywhois/table")
@app.route("/pywhois/table/<amount>")
def findMany(amount=10):
  try:
    recordList = db.pywhois.find({}, {"_id":False}).sort("time", -1).limit(int(amount))  # The -1 means from soonest to latest
    return json_util.dumps(recordList) # Only return the amount requested because of the limit above
  except:
    return json.dumps({"Error": "There was an error returning the information to you. My apologies"})
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

