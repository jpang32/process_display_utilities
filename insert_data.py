from mongo_connect import Connect
from pymongo import MongoClient
import json
import bson
from sample_timeseries_data import create_sample

connection = Connect.get_connection()

db = connection['process-info']

print(db)
#json_obj = json.load(open('sample_data/sample_18052022_213746.json'))
db['cpu-data'].insert_many(create_sample())