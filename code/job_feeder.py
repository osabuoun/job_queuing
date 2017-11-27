import sys 
sys.path.append('..')

import job_operations    
task_id = sys.argv[1]
for x in range(1,30):
	job_operations.add.delay(task_id, x, x + 1)