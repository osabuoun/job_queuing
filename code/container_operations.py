from __future__ import absolute_import, unicode_literals
from queuing_manager import container_app
from pprint import pprint
from threading import Thread
import time, sys
import shlex, subprocess

print("I'm starting the Container Operations")

job_workers = []

def worker(container):
	# Arguments you give on command line
	print("---------------------- worker_main ----------------------")
	output = subprocess.check_output(['python3','job_queuing_worker.py', str(container)])
	print(output)
	print("---------------------- worker_main End ----------------------")

@container_app.task
def add(container):
	print("**************************************")
	print(container)
	job_worker_thread = Thread(target = worker, args = (container,))
	job_worker_thread.start()
	job_workers.append(job_worker_thread)
	print("**************Back from worker ************")
