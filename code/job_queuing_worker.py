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
		broker	= 	'pyamqp://guest@' + '127.0.0.1' + '//',
		backend	=	'redis://' + '127.0.0.1' + ':6379/1',
		#broker	= 	'pyamqp://admin:mypass@' + 'rabbit' + '//',
		#backend	=	'redis://' + 'redis' + ':6379/1',
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

#def start(container):
if __name__ == '__main__':
	print(" ----------- I'm starting the Job Worker for the container " )
	job_app = init()
	job_worker = worker.worker(app=job_app)
	job_options = {
		'hostname'	: "job_" + worker_name ,
		'queues'	: [job_queue_name],
		'loglevel': 'INFO',
		'traceback': True,

	}
	'''
	argv = [
        'worker','-A','job_queuing_worker',
        '--loglevel=info']
	#job_app.start()
	job_app.worker_main(argv)
	'''
	job_worker.run(**job_options)
