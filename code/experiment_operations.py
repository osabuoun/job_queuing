from __future__ import absolute_import, unicode_literals
from pprint import pprint
import time, sys

from experiment_manager import experiment_app
import monitoring

print("I'm starting the Experiment Operations")
index=0
customer_services = {}

@experiment_app.task(bind=True)
def add(self, experiment_id, customer_service_name, experiment_params):
	global index 
	print("**************************************" + str(index))
	customer_services[customer_service_name] = {'experiment_id':experiment_id, 'experiment_params':experiment_params}
	print("A new experiment has just been added")
	print(str(experiment_id))
	print(str(customer_service_name))
	print(str(experiment_params))
	print("**************************************")
	print(str(customer_services))
	index = index + 1

