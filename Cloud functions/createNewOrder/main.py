import pymongo
from pymongo import MongoClient
from bson.json_util import dumps
import os
import requests
import json

def create_new_order(request):

  request_json = request.get_json(silent=True)

  if(request_json and 'order_data' in request_json ):
    order_data = request_json['order_data']
  else:
    order_data = request.args.get("order_data")

  mongoURL = requests.get("https://us-central1-teak-amphora-328909.cloudfunctions.net/getMongoURL")

  client = MongoClient(mongoURL.text)

  db=client.AD_Assignment

  collection = db.Orders

  orderID = int(collection.count()) + 1

  new_order = {"orderID":str(orderID), "customerID":order_data['userID'], "orderContents":order_data["basket_data"], "addresses":order_data["address_data"], "billing":order_data["cost_data"], "orderStatus":"New", "trackingURL":"unassigned", "orderDate":order_data["order_date"]}

  collection.insert_one(new_order)

  return dumps(orderID)