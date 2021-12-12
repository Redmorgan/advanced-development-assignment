import pymongo
from pymongo import MongoClient
from bson.json_util import dumps
import os
import requests
import json

def update_order(request):

  request_json = request.get_json(silent=True)

  if(request_json and 'update_data' in request_json):
    update_data = request_json['update_data']
  else:
    update_data = request.args.get("update_data")

  mongoURL = requests.get("https://us-central1-teak-amphora-328909.cloudfunctions.net/getMongoURL")

  client = MongoClient(mongoURL.text)

  db=client.AD_Assignment

  collection = db.Orders

  if( update_data['trackingURL'] == "" ):
    update_data['trackingURL'] = "unassigned"

  filter = { 'orderID': update_data['orderID'] }

  updatedValues = { "$set":{ 'orderStatus':update_data['orderStatus'], 'trackingURL':update_data['trackingURL'] } }

  try:
    collection.update_one(filter, updatedValues)
    return "updated"
  except:
    return "error updating, try again."
