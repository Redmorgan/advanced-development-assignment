import pymongo
from pymongo import MongoClient
from bson.json_util import dumps
import os
import requests
import json

def get_product_list(request):
  client = MongoClient("mongodb+srv://will:Zngb78xdEE8bqliz@advanceddevelopmentunit.ow0lz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

  db=client.AD_Assignment

  myCursor=db.Products.find({})

  list_cur=list(myCursor)
  print(list_cur)

  json_data=dumps(list_cur)

  return json_data
 
