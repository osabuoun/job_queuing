from __future__ import absolute_import, unicode_literals
import shlex, sys, time, docker, subprocess

from pprint import pprint
from threading import Thread
from pprint import pprint
from docker import types
import monitoring
import redis
redis_db = redis.StrictRedis(host="localhost", port=6379, db=10)

def start(worker):
	print("**************************************")
	print("Starting container feeder")
	container_list = {}
	client = docker.from_env()
	while True:
		print("A new try to find containers")
		customer_services = redis_db.keys()
		print(str(customer_services))
		for container in client.containers.list():
			container_obj = {}
			try:
				container_long_id = container.attrs['Id']
				container_service_name = container.attrs['Config']['Labels']['com.docker.swarm.service.name']
				container_state_running = container.attrs['State']['Running']
				if (container_state_running != True):
					print("Container isn't running")
					continue
				if (container_service_name not in customer_services):
					#print("Container " + container_long_id + " belongs to non-watched service")
					continue
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