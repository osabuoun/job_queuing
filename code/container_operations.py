from __future__ import absolute_import, unicode_literals
from container_queuing_worker import container_app, container_queue_name
import job_queuing_worker
import time
from threading import Thread

print("I'm starting the Container Operations")

job_workers = []

def worker(container):
    # Arguments you give on command line
    argv = [
        'worker','-A','job_queuing_worker',
        '--loglevel=info']
    job_queuing_worker.job_app.worker_main(argv)

@container_app.task
def add(container):
	print("**************************************")
	print(container)
	if (len(job_workers) < 1):
		job_worker_thread = Thread(target = worker, args = (container,))
		job_worker_thread.start()
		job_workers.append(job_worker_thread)
		print("**************************************")

@container_app.task
def add_old(task, x, y):
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