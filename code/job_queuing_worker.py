from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery.bin import worker
from threading import Thread

import time
import sys 
sys.path.append('..')
worker_name = sys.argv[1]
job_queue_name 			= 'job_queue'

def init():
	job_app = Celery('job_app',
		broker	= 	'pyamqp://admin:mypass@' + 'rabbit' + '//',
		backend	=	'redis://' + 'redis' + ':6379/1',
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

job_app = init()

def start():
	print("I'm starting the Job Worker")
	job_app = init()
	job_worker = worker.worker(app=job_app)
	job_options = {
		'hostname'	: "job_" + worker_name ,
		'queues'	: [job_queue_name],
		'loglevel': 'INFO',
		'traceback': True,

	}
	job_worker.run(**job_options)
	#job_app.start()
