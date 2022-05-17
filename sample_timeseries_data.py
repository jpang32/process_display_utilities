import subprocess
from datetime import timezone
import datetime
import json
import time

#result = subprocess.run('ps aux | grep WindowServer', shell=True, stdout=subprocess.PIPE)
#print(f'{result.stdout.decode("utf-8").split()[2]}')
process_name = 'WindowServer'
entry_list = []

for i in range(20):
	result = subprocess.run(f'ps aux | grep {process_name}', shell=True, stdout=subprocess.PIPE)
	result = result.stdout.decode('utf-8').split('\n')[0].split()

	dt = datetime.datetime.now(timezone.utc)
	utc_time = dt.replace(tzinfo=timezone.utc)
	utc_timestamp = utc_time.timestamp()

	entry = {
		'metadata' : 
			{'start_date': result[8], 
			 'cpu_time': result[9], 
			 'process_name': process_name,
			 'process_command': ' '.join(result[10:])
			},
		'cpu' : result[2],
		'timestamp' : utc_timestamp
	}
	entry_list.append(entry)

	print(entry)

	time.sleep(1)

json_object = json.dumps(entry_list, indent=4)
print(f'Output json: \n{entry_list}')

output_file_name = datetime.datetime.now().strftime('%d%m%Y_%H%M%S')
with open(f'sample_data/sample_{output_file_name}.json', "w") as outfile:
    outfile.write(json_object)
