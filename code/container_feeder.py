import sys 
sys.path.append('..')

import container_operations    
task_id = sys.argv[1]
for x in range(1,10):
	container_operations.add.delay(task_id, x, x + 1)