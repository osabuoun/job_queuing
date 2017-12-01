from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery.bin import worker
import time, sys
from threading import Thread
import container_feeder, config.parameters as _params
experiment_queue 	= 'experiment_queue'
customer_services = {}

import redis
redis_db = redis.StrictRedis(host="localhost", port=6379, db=10)

def init_experiment_worker():
	print(_params.broker())
	print()
	experiment_app = Celery('experiment_app',
		broker	= 	_params.broker() ,
		backend	=	_params.backend(2),
		include = ['experiment_manager']
	)

	experiment_app.conf.update(
		task_routes = {
			'experiment_manager.add': {'queue': experiment_queue},
		},
		task_default_queue = 'experiment_default_queue',
		result_expires=3600,
		task_serializer = 'json',
		accept_content = ['json'],
		worker_concurrency = 1,
		worker_prefetch_multiplier = 1,
		task_acks_late = True,
		task_default_exchange = 'experiment_exchange',
		task_default_routing_key = 'experiment_routing_key' ,
	)
	return experiment_app

experiment_app = init_experiment_worker()

@experiment_app.task(bind=True)
def add(self, experiment_id, customer_service_name, experiment_params):
	print("**************************************" )
	redis_db.set(customer_service_name, {'experiment_id':experiment_id, 'experiment_params':experiment_params})
	#customer_services[customer_service_name] = {'experiment_id':experiment_id, 'experiment_params':experiment_params}
	print("A new experiment has just been added")
	print(str(experiment_id))
	print(str(customer_service_name))
	print(str(experiment_params))
	print("**************************************")
	print(str(customer_services))

def start_experiment_worker(worker):
	print("I'm starting the Experiment Worker")
	experiment_app = init_experiment_worker()
	experiment_worker = worker.worker(app=experiment_app)
	experiment_options = {
		'hostname'	: "experiment_manager",
		'queues'	: [experiment_queue],
		'loglevel': 'INFO',
		'traceback': True,
	}
	experiment_worker.run(**experiment_options)

if __name__ == '__main__':
	experiment_worker_thread = Thread(target = start_experiment_worker, args = (worker,))
	experiment_worker_thread.start()
	container_feeder_thread = Thread(target = container_feeder.start, args = (worker,))
	container_feeder_thread.start()
