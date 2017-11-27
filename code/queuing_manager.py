from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery.bin import worker
import time, sys

container_queue_name 	= 'container_queue'

def init_container_worker():
	container_app = Celery('container_app',
		#broker	= 	'pyamqp://guest@' + '127.0.0.1' + '//',
		#backend	=	'redis://' + '127.0.0.1' + ':6379/0',
		broker	= 	'pyamqp://admin:mypass@' + 'rabbit' + '//',
		backend	=	'redis://' + 'redis' + ':6379/0',
		include	=	['container_operations'])

	container_app.conf.update(
		task_routes = {
			'container_operations.add': {'queue': container_queue_name},
		},
		task_default_queue = 'container_default_queue',
		result_expires=3600,
		task_serializer = 'json',
		accept_content = ['json'],
		worker_concurrency = 1,
		worker_prefetch_multiplier = 1,
		task_acks_late = True,
		task_default_exchange = 'container_exchange',
		task_default_routing_key = 'container_routing_key' ,
	)
	return container_app

container_app = init_container_worker()

def start_container_worker(worker):
	print("I'm starting the Container Worker")
	container_app = init_container_worker()
	container_worker = worker.worker(app=container_app)
	container_options = {
		'hostname'	: "queuing_manager",
		'queues'	: [container_queue_name],
		'loglevel': 'INFO',
		'traceback': True,
	}
	container_worker.run(**container_options)

if __name__ == '__main__':
	start_container_worker(worker)


