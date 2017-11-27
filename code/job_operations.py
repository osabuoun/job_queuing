from __future__ import absolute_import, unicode_literals
from job_queuing_worker import job_app
import time

print("I'm starting the Job Operations")

@job_app.task
def add(task, x, y):
	print("New Job Add - Task: " + task + " - " + str(x) + " - " + str(y))
	time.sleep(5)
	print("New Job Result - after " + task + " - " + str(x) + " - " + str(y))
	return x + y
