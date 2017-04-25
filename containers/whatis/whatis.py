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

@app.route('/')
def help():
    help = "Format for accessing. 'http://ipAddress/whatis/port/proto(optional)\nThe purpose of this is to find out what a port and protocol means."
    return help
@app.route('/whatis/<port>')
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
    return json.dumps({"status":"Not Found", "message":"This port and protocol pair could not be found in the database, it could be a nonstandard port or new."})




def findRecord(port, proto=None):

    try:
        if proto is not None:
            record = db.whatis.find({'Port Number': port, "Transport Protocol": proto})
        else:
            record = db.whatis.find({'Port Number': port})

        # Returns a list because it can technically have multiple records if they don't have the protocol defined.
        return [x for x in record]
    except:
        return None

@app.route("/whatis/table")
@app.route("/whatis/table/<amount>")
def findMany(amount=10):
  portsList = [443,3389,162,80,23,123,22,80,2000,3,1,25,5060,137,445,2323,161,110,88,5355,139,445]
  resultsList = []
  try:
    resultsList.append(db.whatis.find_one({"Port Number": 53, "Transport Protocol":"udp"}, {"_id":False})) # 53 doesn't use tcp
    for i in portsList[:amount-1]:
      resultsList.append(db.whatis.find_one({"Port Number":i, "Transport Protocol":"tcp"},{"_id":False}))

    return json_util.dumps(resultsList) # Only return the amount requested because of the limit above
  except:
    return json.dumps({"Error": "There was an error returning the information to you. My apologies"})
if __name__ == "__main__":
    app.run(host='0.0.0.0',  debug=True)

