import os
from flask import Flask, redirect, url_for, render_template, request
import json
from pymongo import MongoClient
from bson import json_util
import re
app = Flask(__name__)

# Connection to database
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
    # It'll inevitably take up extra space but that's fine for the case of sameness
    mongoRecord = {headers[i]:lineList[i] for i in range(len(headers))}
    # Dumps each record to the db
    db.whatis.insert(mongoRecord)

@app.route('/whatis')
def help():
    help = "Format for accessing. 'http://ipAddress/whatis/port/proto(optional)\nThe purpose of this is to find out what a port and protocol means."
    return help
@app.route('/whatis/<port>/<proto>')
def whatis(port, proto=None):
    # I don't want to try this if the port isn't a number.
    # Should be quick since the regex is already compiled for me
    if number.match(port):
        port = int(port)
    else:
        # Tell them nice try
        return json.dumps({"status":"Failure", "error":"Port was not an integer"})
    # These are the only Protocols in the file, The last two are very uncommon so to reduce already short search terms I moved them to the end
    if proto not in ['tcp','udp', None, '', 'sctp', 'dccp',]:
        return json.dumps({"status": "Failure", "error": "Protocol is not a listed type."})
    # There will need to be different logic based on the port and protocol if it exists
    #if (proto is not None):
    findResult = findRecord(port, proto)
    if (findResult is not None):
        return json_util.dumps({"status":"Found", "result": findResult})
    return json.dumps({"status":"Not Found", "message":"This port and protocol pair couldn't be found could not be found in the database, it could be a nonstandard port or new."})




def findRecord(port, proto=None):

    try:
        if proto is not None:
            record = db.whatis.find({'Port Number':port})
        else:
            record = db.whatis.find({'Port Number':port, "Transport Protocol": proto})
        # Returns a list because it can technically have multiple records if they don't have the protocol defined.
        return [x for x in record]
    except:
        return None


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)

