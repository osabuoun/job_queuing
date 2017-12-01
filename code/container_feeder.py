from __future__ import absolute_import, unicode_literals
import shlex, sys, time, docker, subprocess, ast, redis

from pprint import pprint
from threading import Thread
from pprint import pprint
from docker import types
import monitoring
from config.parameters import backend_experiment_db

job_workers = []
node_id = "no_id_3"
customer_services = {}

def worker(container):
	# Arguments you give on command line
	global node_id
	monitoring.add_worker(node_id, container["service_name"])
	output = subprocess.check_output(['python3','jqueuing_worker.py', str(node_id) ,str(container)])
	monitoring.terminate_worker(node_id, service_name)
	print("Worker_main Output: " + str(output))

def add(container):
	print("**************************************")
	print(container)
	job_worker_thread = Thread(target = worker, args = (container,))
	job_worker_thread.start()
	job_workers.append(job_worker_thread)
	print("**************Back from worker ************")

def start(node_id_t):
	global node_id
	node_id = node_id_t
	print("Starting container feeder")
	container_list = {}
	client = docker.from_env()
	while True:
		for container in client.containers.list():
			container_obj = {}
			try:
				container_long_id = container.attrs['Id']
				container_service_name = container.attrs['Config']['Labels']['com.docker.swarm.service.name']
				container_state_running = container.attrs['State']['Running']
				if (container_state_running != True):
					print("Container isn't running")
					continue
				if (not backend_experiment_db.exists(container_service_name)):
					print("Container " + container_long_id + " belongs to non-watched service")
					continue
				experiment = ast.literal_eval(backend_experiment_db.get(container_service_name))
				#print("Container " + container_long_id + " belongs to a watched service")
				if (container_long_id in container_list):
					#print("Container " + container_long_id + " has been added previously")
					continue
				container_obj = {
					'id_long': container_long_id,
					'name': container.attrs['Name'], 
					'service_id': container.attrs['Config']['Labels']['com.docker.swarm.service.id'],
					'service_name': container_service_name,
					'task_id': container.attrs['Config']['Labels']['com.docker.swarm.task.id'],
					'task_name': container.attrs['Config']['Labels']['com.docker.swarm.task.name'],
					'hostname' : container.attrs['Config']['Hostname'],
					'ip_address': '',
					'created': container.attrs['Created'],
					'started': container.attrs['State']['StartedAt'],
					'experiment_id':experiment['id'], 
					'experiment_params':experiment['params'], 
				}
				try:
					container_obj['ip_address'] = container.attrs['NetworkSettings']['Networks']['bridge']['IPAddress']
					add(container_obj)
					container_list[container_long_id] = container_obj
					pprint(container_obj)
				except Exception as e:
					print("An error happened while sending the container to the Agent")
					pass
			except Exception as e:
				#print("It isn't a swarm service's container")
				pass
		time.sleep(5)