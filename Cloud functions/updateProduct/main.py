import pymongo
from pymongo import MongoClient
from bson.json_util import dumps
import os
import requests
import json

def update_product(request):

  request_json = request.get_json(silent=True)

  if(request_json and 'product_data' in request_json):
    product_data = request_json['product_data']
  else:
    product_data = request.args.get("product_data")

  mongoURL = requests.get("https://us-central1-teak-amphora-328909.cloudfunctions.net/getMongoURL")

  client = MongoClient(mongoURL.text)

  db=client.AD_Assignment

  collection = db.Products

  filter = { 'id': product_data['originalID'] }

  if(product_data['productUrl'] == ""):
    updatedValues = { "$set":{ "id":product_data['id'], "name":product_data['name'], "desc":product_data['desc'], "price":product_data['price']} }
  else:
    updatedValues = { "$set":{ "id":product_data['id'], "name":product_data['name'], "desc":product_data['desc'], "productUrl":product_data['productUrl'], "price":product_data['price']} }

  try:
    collection.update_one(filter, updatedValues)
    return "updated"
  except:
    return "error updating, try again."


