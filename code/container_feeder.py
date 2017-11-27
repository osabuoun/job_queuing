import sys,time, docker, subprocess
from pprint import pprint
from docker import types

import container_operations    


task_id = sys.argv[1]
service_name = 'customer_app'
client = docker.from_env()
index = 1

print("--------------- Checkpoint #1")
mode = types.ServiceMode(mode='replicated', replicas= index)
print("--------------- Checkpoint #2")
env = ["SERVER=172.17.0.1", "PORT=8777" , "INSTANCE=123"]
print("--------------- Checkpoint #3")
#output = subprocess.check_output(['docker','service', 'create', 'queuing_simple' ])
#print(output)


#service = client.services.create("queuing_simple", command=None, env= env, mode= mode)
print("--------------- Checkpoint #4")
#print(service.id)
#print(service.name)
#print(service.tasks)
container_list = {}
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
			if (container_service_name != service_name):
				print("Container " + container_long_id + " belongs to different service")
				continue
			if (container_long_id in container_list):
				print("Container " + container_long_id + " has been added previously")
				continue
			container_obj = {
				'id_long': container_long_id,
				'name': container.attrs['Name'], 
				'service_id': container.attrs['Config']['Labels']['com.docker.swarm.service.id'],
				'task_id': container.attrs['Config']['Labels']['com.docker.swarm.task.id'],
				'task_name': container.attrs['Config']['Labels']['com.docker.swarm.task.name'],
				'hostname' : container.attrs['Config']['Hostname'],
				'ip_address': '',
				'created': container.attrs['Created'],
				'started': container.attrs['State']['StartedAt'], 
				}
			try:
				container_obj['ip_address'] = container.attrs['NetworkSettings']['Networks']['bridge']['IPAddress']
				container_operations.add.delay(container_obj)
				container_list[container_long_id] = container_obj
				pprint(container_obj)
			except Exception as e:
				print("An error happened while sending the container to the Agent")
				pass
		except Exception as e:
			print("It isn't a swarm service's container")

	time.sleep(5)

'''
for x in range(1,10):
	container_operations.add.delay(task_id, x, x + 1)

id = 0
while(1):
	print(id)
	id = id+1
	time.sleep(1)
'''