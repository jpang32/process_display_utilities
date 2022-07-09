"""
    Takes non-bucketized data about cpu usage and buckets it
    by day.

    If stream data is ever run and stores non-bucketized data
    to mongodb, this script can be run to bucketize it by day,
    similar to how data is streamed from stream_data_bucket.py.
"""

from itertools import groupby
from mongo_connect import Connect
from pymongo import MongoClient
import json
import bson
from sample_timeseries_data import create_sample
import pymongo
from datetime import datetime
from datetime import timedelta

connection = Connect.get_connection()

db = connection['process-info']

former_db = 'cpu-data'
destination_db = 'cpu-data-buckets'

start_date = '5/20/2022'
start_date = datetime.strptime(start_date, '%m/%d/%Y')
end_date = (datetime.now() + timedelta(days=1)).strftime('%m/%d/%Y') 
end_date = datetime.strptime(end_date, '%m/%d/%Y')

boundaries = []
for day in range(end_date.day - start_date.day + 1):
    boundaries.append(start_date + timedelta(days=day))

print(boundaries)
aggregation = db[former_db].aggregate([
    {
        "$sort": {
            "timestamp": pymongo.ASCENDING
        }
    },
    {
        '$bucket' : {
            'groupBy': '$timestamp',
            'boundaries': boundaries,
            'output': { 
                'count': {'$sum': 1},
                'items' : {
                    '$push' : {
                        'metadata': '$metadata',
                        'timestamp': '$timestamp',
                        'cpu': {'$toDouble' : '$cpu'}
                    }
                }
            }
        }
    }
]
)

db[destination_db].insert_many(
    aggregation
)