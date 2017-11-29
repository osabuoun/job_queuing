import sys 
sys.path.append('..')

import job_operations    
job_id = sys.argv[1]
for x in range(1,500):
	job_operations.add.delay(
		job_id, 
		["python3","app.py"], 
		[
			{"id":"id_1", "data":["127.0.0." + str(x)]}
		]
	)