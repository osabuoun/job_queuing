from __future__ import absolute_import, unicode_literals
from job_queuing_worker import job_app
import job_queuing_worker
import time, shlex, subprocess

print("Job Operations - Started")

@job_app.task(bind=True)
def add(self, job_id, script_command, script_params):
	log_file =  "./log/" + self.request.hostname + ".log"
	container_id = self.request.hostname.split("@")[1]
	with open(log_file, "a") as myfile:
		myfile.write("worker_name: " + job_queuing_worker.worker_name + "\n") 
		myfile.write("New Job: " + job_id + "\n") 
		myfile.write("Command: " + str(script_command) + "\n")
		myfile.write("Parameters: " + str(len(script_params)) + "\n")
		for script_param in script_params:
			myfile.write("Parameters: " + str(script_param) + "\n")
		myfile.write("-------------------------------------\n")
		for script_param in script_params:
			command = ['docker','exec', container_id] + script_command + script_param
			output = subprocess.check_output(command)
			myfile.write("output: " + str(output) + "\n")
