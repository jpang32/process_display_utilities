from mongo_connect import Connect
import subprocess
import datetime
import time


connection = Connect.get_connection()
db = connection['process-info']

print(db)

coll = db['cpu-data']

process_name = 'WindowServer'
while True:
    result = subprocess.run(f'ps aux | grep {process_name}', shell=True, stdout=subprocess.PIPE)
    result = result.stdout.decode('utf-8').split('\n')[0].split()
    
    dt = datetime.datetime.now()

    entry = {
        'metadata' : 
            {'start_date': result[8], 
            'cpu_time': result[9], 
            'process_name': process_name,
            'process_command': ' '.join(result[10:])
            },
        'cpu' : result[2],
        'timestamp' : dt
    }

    #json_obj = json.load(open('sample_data/sample_18052022_213746.json'))
    db['cpu-data'].insert_one(entry)
    time.sleep(60)