from mongo_connect import Connect
import subprocess
from datetime import datetime
from datetime import timedelta
import time


connection = Connect.get_connection()
db = connection['process-info']

print(db)

coll = db['cpu-data']

process_name = 'WindowServer'
while True:
    result = subprocess.run(f'ps aux | grep {process_name}', shell=True, stdout=subprocess.PIPE)
    result = result.stdout.decode('utf-8').split('\n')[0].split()

    dt = (datetime.now()).strftime('%m/%d/%Y') 
    dt = datetime.strptime(dt, '%m/%d/%Y')

    upsert_result = db['cpu-data-buckets'].update_one(
        {
            '_id': dt,
        },
        {
            '$setOnInsert': {
                '_id': dt,
                'count': 0,
                'items': []
            }
        },
        True
    ) 

    if upsert_result.upserted_id:
        print(f'New bucket created: {dt}')

    update_result = db['cpu-data-buckets'].update_one(
        {
            '_id': dt
        },
        {
            '$push': {
                'items': {
                    'metadata' : 
                    {
                        'start_date': result[8], 
                        'cpu_time': result[9], 
                        'process_name': process_name,
                        'process_command': ' '.join(result[10:])
                    },
                    'cpu' : float(result[2]),
                    'timestamp' : dt
                } 
            },
            '$inc': {'count': 1}
        }
    )
    
    time.sleep(60)