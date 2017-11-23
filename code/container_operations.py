from __future__ import absolute_import, unicode_literals
from container_queuing_worker import container_app, container_queue_name
import job_queuing_worker
import time

print("I'm starting the Container Operations")

@container_app.task
def add(task, x, y):
	container_app.control.cancel_consumer('add_queue', reply=True)
	print("New Container Add - Task: " + task + " - " + str(x) + " - " + str(y))
	time.sleep(1)
	job_queuing_worker.start()
	print("New Container Result - after " + task + " - " + str(x) + " - " + str(y))


	container_app.control.add_consumer(
		queue='add_queue',
		reply=True,
	)
	return x + y