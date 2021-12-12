import pymongo
from pymongo import MongoClient
from bson.json_util import dumps
import os
import requests
import json

def get_basket_items_by_id(request):

  request_json = request.get_json(silent=True)

  if(request_json and 'basket' in request_json):
    basket = request_json['basket']
  else:
    basket = request.args.get("basket")

  mongoURL = requests.get("https://us-central1-teak-amphora-328909.cloudfunctions.net/getMongoURL")

  client = MongoClient(mongoURL.text)

  db=client.AD_Assignment

  basketProducts = []

  for item in basket:
    
    myCursor=db.Products.find({"id":item['productID']})
    
    subtotal = "{:.2f}".format(myCursor[0]['price'] * item['quantity'])

    basketItem = {"product":myCursor, "quantity":item['quantity'], "subtotal":subtotal}

    basketProducts.append(basketItem)

  json_data=dumps(basketProducts)

  return json_data
 
 
