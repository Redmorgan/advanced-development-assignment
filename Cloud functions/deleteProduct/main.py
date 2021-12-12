import pymongo
from pymongo import MongoClient
from bson.json_util import dumps
import os
import requests
import json

def delete_product(request):

  request_json = request.get_json(silent=True)

  if(request_json and 'product_id' in request_json):
    productID = request_json['product_id']
  else:
    productID = request.args.get("product_id")

  mongoURL = requests.get("https://us-central1-teak-amphora-328909.cloudfunctions.net/getMongoURL")

  client = MongoClient(mongoURL.text)

  db=client.AD_Assignment

  collection = db.Products

  delete_product = {"id":productID}

  collection.delete_one(delete_product)

  return "deleted"