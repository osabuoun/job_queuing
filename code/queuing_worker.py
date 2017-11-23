from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery.bin import worker
from threading import Thread

import time
import sys 
sys.path.append('..')
worker_name = sys.argv[1]
job_queue_name 			= 'job_queue'
container_queue_name 	= 'container_queue'


def init_container_worker():
	container_app = Celery('container_app',
		broker	= 	'pyamqp://guest@localhost//',
		backend	=	'redis://localhost:6379/0',
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

def init_job_worker():
	job_app = Celery('job_app',
		broker  =   'pyamqp://guest@localhost//',
		backend =   'redis://localhost:6379/1',
		include =   ['job_operations'])

	job_app.conf.update(
		task_routes = {
			'job_operations.add': {'queue': job_queue_name},
		},
		task_default_queue = 'job_default_queue',
		result_expires=3600,
		task_serializer = 'json',
		accept_content = ['json'],
		worker_concurrency = 1,
		worker_prefetch_multiplier = 1,
		task_acks_late = True,
		task_default_exchange = 'job_exchange',
		task_default_routing_key = 'job_routing_key' ,
	)
	return job_app

job_app = init_job_worker()

def start_container_worker(worker):
	print("I'm starting the Container Worker")
	container_app = init_container_worker()
	container_worker = worker.worker(app=container_app)
	container_options = {
		'hostname'	: "container_" + worker_name,
		'queues'	: [container_queue_name],
		'loglevel': 'INFO',
		'traceback': True,
	}
	container_worker.run(**container_options)

def start_job_worker(worker):
	print("I'm starting the Job Worker")
	job_app = init_job_worker()
	job_worker = worker.worker(app=job_app)
	job_options = {
		'hostname'	: "job_" + worker_name ,
		'queues'	: [job_queue_name],
		'loglevel': 'INFO',
		'traceback': True,

	}
	job_worker.run(**job_options)
	#job_app.start()

if __name__ == '__main__':
	container_worker_thread = Thread(target = start_container_worker, args=(worker,))
	#container_worker_thread.start()

	job_worker_thread = Thread(target = start_job_worker, args=(worker,))
	job_worker_thread.start()



