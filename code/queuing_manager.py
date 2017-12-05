from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery.bin import worker
import time, sys
from threading import Thread
import container_feeder, config.parameters as _params
import experiment_operations, experiment_receiver

node_id = "id_1"
jqueue_name 	= 'jqueuing_queue'

def init_jqueuing_worker():
	jqueuing_app = Celery('jqueuing_app',
		broker	= 	_params.broker() ,
		backend	=	_params.backend(0),
		include	=	['experiment_operations'])

	jqueuing_app.conf.update(
		task_routes = {
			'experiment_operations.add': {'queue': jqueue_name},
		},
		task_default_queue = 'jqueuing_default_queue',
		result_expires=3600,
		task_serializer = 'json',
		accept_content = ['json'],
		worker_concurrency = 1,
		worker_prefetch_multiplier = 1,
		task_acks_late = True,
		task_default_exchange = 'jqueuing_exchange',
		task_default_routing_key = 'jqueuing_routing_key' ,
	)
	return jqueuing_app

jqueuing_app = init_jqueuing_worker()

def start_jqueuing_worker(worker):
	print("I'm starting the JQueing Worker")
	jqueuing_app = init_jqueuing_worker()
	jqueuing_worker = worker.worker(app=jqueuing_app)
	jqueuing_options = {
		'hostname'	: "queuing_manager",
		'queues'	: [jqueue_name],
		'loglevel': 'INFO',
		'traceback': True,
	}
	jqueuing_worker.run(**jqueuing_options)

if __name__ == '__main__':
	worker_thread = Thread(target = start_jqueuing_worker, args = (worker,))
	worker_thread.start()
	experiment_receiver_thread = Thread(target = experiment_receiver.start, args = ())
	experiment_receiver_thread.start()
	container_feeder_thread = Thread(target = container_feeder.start, args = (node_id,))
	container_feeder_thread.start()