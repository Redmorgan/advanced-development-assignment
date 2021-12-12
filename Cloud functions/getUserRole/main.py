import pymongo
from pymongo import MongoClient
from bson.json_util import dumps
import os
import requests
import json

def get_user_role(request):

  request_json = request.get_json(silent=True)

  if(request_json and 'id' in request_json):
    userID = request_json['id']
  else:
    userID = request.args.get("id")

  mongoURL = requests.get("https://us-central1-teak-amphora-328909.cloudfunctions.net/getMongoURL")

  client = MongoClient(mongoURL.text)

  db=client.AD_Assignment

  myCursor=db.Users.find({"id":userID})

  list_cur=list(myCursor)

  json_data=dumps(list_cur)

  return json_data
 
