import pymongo
from pymongo import MongoClient
from bson.json_util import dumps
import os
import requests
import json

def create_product(request):

  request_json = request.get_json(silent=True)

  if(request_json and 'product_data' in request_json ):
    product_data = request_json['product_data']
  else:
    product_data = request.args.get("product_data")

  mongoURL = requests.get("https://us-central1-teak-amphora-328909.cloudfunctions.net/getMongoURL")

  client = MongoClient(mongoURL.text)

  db=client.AD_Assignment

  collection = db.Products

  useCount = collection.count({"id":product_data['id']})

  if useCount == 1:

    return "exists"

  else:

    new_product = {"id":product_data['id'], "name":product_data['name'], "desc":product_data["desc"], "productUrl":product_data["productUrl"], "price":product_data["price"]}

    collection.insert_one(new_product)

    return "created"