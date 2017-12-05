from __future__ import absolute_import, unicode_literals
from pprint import pprint
import time, sys, redis, random

from queuing_manager import jqueuing_app
import monitoring, config.parameters as _params

from config.parameters import backend_experiment_db

print("I'm starting the Experiment Operations")
index=0
customer_services = {}

def add_experiment(experiment):
	print("experiment: " + str(experiment))
	return add(experiment['service_name'], experiment['experiment_params'])

@jqueuing_app.task(bind=True)
def add(self, customer_service_name, experiment_params):
	print("**************************************")
	if (backend_experiment_db.exists(customer_service_name)):
		result = "\n" + "Customer Service " + customer_service_name + " already registered" + "\n"
		return result
	experiment_id = "exp_" + str(int(round(time.time() * 1000))) + "_" + str(random.randrange(100, 999))
	backend_experiment_db.set(customer_service_name, {'experiment_id':experiment_id, 'experiment_params':experiment_params})
	result  = "\n" + "**************************************" + "\n"
	result += "A new experiment has just been added" + "\n"
	result += "ID: " + str(experiment_id) + "\n" 
	result += "Service Name: " + str(customer_service_name) + "\n" 
	result += "Parameters: " + str(experiment_params) + "\n" 
	result += "**************************************" + "\n"
	return result
