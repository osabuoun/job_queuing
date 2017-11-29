from __future__ import absolute_import, unicode_literals
import time, shlex, subprocess, random

from job_queuing_worker import job_app
import job_queuing_worker as jqw
import monitoring

print("Job Operations - Started")

@job_app.task(bind=True)
def add(self, job_id, task_command, job_params):
	job_start_time = time.time()

	params = self.request.hostname.split("@")[1]
	node_id = params.split("##")[0]
	container_id = params.split("##")[1]

	monitoring.run_job(node_id, jqw.worker_name, job_id)

	log_file =  "./log/" + self.request.hostname + ".log"

	with open(log_file, "a") as myfile:
		myfile.write("node_id: " + jqw.node_id + "\n") 
		myfile.write("worker_name: " + jqw.worker_name + "\n") 
		myfile.write("New Job: " + job_id + "\n") 
		myfile.write("Command: " + str(task_command) + "\n")
		myfile.write("Parameters: " + str(len(job_params)) + "\n")
		for task_params in job_params:
			myfile.write("Parameters: " + str(task_params) + "\n")
		myfile.write("-------------------------------------\n")
		time.sleep(random.randrange(10, 100))
		for task_params in job_params:
			task_start_time = time.time()
			task_id = task_params["id"]
			task_data = task_params["data"]
			monitoring.run_task(node_id, jqw.worker_name, job_id, task_id)
			command = ['docker','exec', container_id] + task_command + task_data
			monitoring.terminate_task(node_id, jqw.worker_name, job_id, task_id, task_start_time)
			output = subprocess.check_output(command)
			myfile.write("output: " + str(output) + "\n")
	monitoring.terminate_job(node_id, jqw.worker_name, job_id, job_start_time)