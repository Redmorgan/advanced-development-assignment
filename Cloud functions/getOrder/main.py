import pymongo
from pymongo import MongoClient
from bson.json_util import dumps
import os
import requests
import json

def get_orders(request):

  request_json = request.get_json(silent=True)

  if(request_json and 'request_data' in request_json):
    request_data = request_json['request_data']
  else:
    request_data = request.args.get("request_data")

  mongoURL = requests.get("https://us-central1-teak-amphora-328909.cloudfunctions.net/getMongoURL")

  client = MongoClient(mongoURL.text)

  db=client.AD_Assignment

  if (request_data['amount'] == "All"):

    if (request_data['role'] == "admin"):
      myCursor=db.Orders.find({})
    elif (request_data['role'] == "user"):
      myCursor=db.Orders.find({"customerID":request_data['UID']})
    
    list_cur=list(myCursor)

    for item in list_cur:
      item['orderContents'] = len(item['orderContents'])
      del item['addresses']
    
    json_data=dumps(list_cur)
  
  elif (request_data['amount'] == "Single"):
    myCursor=db.Orders.find({"orderID":request_data['UID']})
    json_data=dumps(myCursor)

  return json_data
 
 
