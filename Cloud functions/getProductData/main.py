import pymongo
from pymongo import MongoClient
from bson.json_util import dumps
import os
import requests
import json

def get_product_data(request):

  request_json = request.get_json(silent=True)

  if(request_json and 'id' in request_json):
    productID = request_json['id']
  else:
    productID = request.args.get("id")

  mongoURL = requests.get("https://us-central1-teak-amphora-328909.cloudfunctions.net/getMongoURL")

  client = MongoClient(mongoURL.text)

  db=client.AD_Assignment

  myCursor=db.Products.find({"id":productID})

  return dumps(myCursor)
 
