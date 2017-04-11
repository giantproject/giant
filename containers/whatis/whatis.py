import os
from flask import Flask, redirect, url_for, render_template, request
import json
import whois
from pymongo import MongoClient
from bson import json_util
import re
app = Flask(__name__)

client = MongoClient(os.environ['DB_1_PORT_27017_TCP_ADDR'], 27017)
db = client.db

# Until we have persistent data I'm going to delete it all
db.whatis.delete_many({})

# Build Database
number = re.compile('^[0-9]+$')
servicesFile = open('services.csv')
headers = servicesFile.readline().strip().split(',')
for line in servicesFile:
    lineList = line.strip().split(',')
    for i, item in enumerate(lineList):
        if number.match(item):
            lineList[i] = int(item)
        else:
            # The data isn't formatted correctly. If it isn't a number then I don't care.
            continue
    # List completion. This just builds a dict object that will ALWAYS have the header fields and will store them
    # It'll inevitably take up extra space but that's find for the case of sameness
    mongoRecord = {headers[i]:lineList[i] for i in range(len(headers))}
    # Dumps them to the db
    db.whatis.insert(mongoRecord)

@app.route('/')
def help():
    help = "Format for accessing. 'https://ipAddress/whatis/port' But anyway You made it here"
    return help
@app.route('/whatis/<port>/<proto>')
def whatis(port, proto=None):
    if number.match(port):
        port = int(port)
    else:
        return json.dumps({"status":"Failure", "error":"Port was not an integer"})
    if proto not in ['tcp','udp', None, '', 'sctp', 'dccp',]:
        return json.dumps({"status": "Failure", "error": "Protocol is not a listed type so you won't find anything anyway"})
    # There will need to be different logic based on the port and protocol if it exists
    if (proto is not None):
        findResult = findRecord(port, proto)
        if (findResult is not None):
          id = findResult.get('_id')
            return json_util.dumps({"status":"Found", "id": str(id), "result": findResult})
        return json.dumps({"status":"Not Found", "message":"This port and protocol pair couldn't be found could not be found in the database, it could be a nonstandard port or new."})




def findRecord(port, proto):
    try:
        record = db.whatis.find_one({'Port Number':port})
        if (record is not None):
            return record
        else:
            return None
    except:
        return None


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)

