import pymongo
from pymongo import MongoClient
from bson.json_util import dumps
import os
import requests
import json

def add_new_user(request):

  request_json = request.get_json(silent=True)

  if(request_json and 'id' in request_json):
    userID = request_json['id']
  else:
    userID = request.args.get("id")

  mongoURL = requests.get("https://us-central1-teak-amphora-328909.cloudfunctions.net/getMongoURL")

  client = MongoClient(mongoURL.text)

  db=client.AD_Assignment

  collection = db.Users

  new_user = {"id":userID, "role":"user"}

  collection.insert_one(new_user)

  return "user"