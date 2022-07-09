"""
	Creates a small (non-bucketized) collection of 
	sample documents that will be pushed to mongodb 
	when insert_data is run.
"""

import subprocess
from datetime import timezone
import datetime
import json
import time
import bson

#result = subprocess.run('ps aux | grep WindowServer', shell=True, stdout=subprocess.PIPE)
#print(f'{result.stdout.decode("utf-8").split()[2]}')

def create_sample(num_samples=20, to_file=False):
	process_name = 'WindowServer'
	entry_list = []

	for i in range(num_samples):
		result = subprocess.run(f'ps aux | grep {process_name}', shell=True, stdout=subprocess.PIPE)
		result = result.stdout.decode('utf-8').split('\n')[0].split()
		
		dt = ''
		if to_file:
			dt = datetime.datetime.now().isoformat()
		else:
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


		entry_list.append(entry)

		print(entry)

		time.sleep(1)

	print(f'Output entries: \n{entry_list}')

	if to_file:
		entry_list = json.dumps(entry_list, indent=4)
		output_file_name = datetime.datetime.now().strftime('%d%m%Y_%H%M%S')
		with open(f'sample_data/sample_{output_file_name}.json', "w") as outfile:
			outfile.write(entry_list)

	return entry_list
