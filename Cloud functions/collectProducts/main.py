import pymongo
from pymongo import MongoClient
from bson.json_util import dumps
import os
import requests
import json

def get_product_list(request):

  mongoURL = requests.get("https://us-central1-teak-amphora-328909.cloudfunctions.net/getMongoURL")

  client = MongoClient(mongoURL.text)

  db=client.AD_Assignment

  myCursor=db.Products.find({})

  list_cur=list(myCursor)
  print(list_cur)

  json_data=dumps(list_cur)

  return json_data
 
