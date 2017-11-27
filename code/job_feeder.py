import sys 
sys.path.append('..')

import job_operations    
task_id = sys.argv[1]
for x in range(1,100):
	job_operations.add.delay(task_id, ["python3","app.py"], [["127.0.0." + str(x)]])