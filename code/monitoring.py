from prometheus_client import Counter, Gauge, Histogram
import time, sys
from datadog import DogStatsd

statsd = DogStatsd(host="127.0.0.1", port=9125)

JQUEUING_WORKER_ADDED_COUNT = 'jqueuing_worker_added_count'
'''
Counter(
    'jqueuing_worker_added_count', 'jqueuing_worker_added_count',
    ['node_id']
)
'''
JQUEUING_WORKER_COUNT = "jqueuing_worker_count" 
'''
Gauge(
    'jqueuing_worker_count', 'jqueuing_worker_count',
    ['node_id']
)
'''

def add_worker(node_id):
	statsd.increment(JQUEUING_WORKER_ADDED_COUNT,
		tags=[
			'node_id:%s' % node_id,
		]
	)
	statsd.increment(node_id,
		tags=[
			'node_id:%s' % node_id,
		]
	)

JQUEUING_WORKER_TERMINATED_COUNT = 'jqueuing_worker_terminated_count'
'''
Counter(
    'jqueuing_worker_terminated_count', 'jqueuing_worker_terminated_count',
    ['node_id']
)
'''
def terminate_worker(node_id):
	statsd.decrement(node_id,
		tags=[
			'node_id:%s' % node_id,
		]
	)
JQUEUING_JOB_RUNNING_COUNT = 'jqueuing_job_running_count'
'''
Gauge(
    'jqueuing_job_running_count', 'jqueuing_job_running_count',
    ['node_id', 'qworker_id', 'job_id']
)
'''

JQUEUING_JOB_ACCOMPLISHED_COUNT = 'jqueuing_job_accomplished_count'
'''
Counter(
    'jqueuing_job_accomplished_count', 'jqueuing_job_accomplished_count',
    ['node_id', 'qworker_id', 'job_id']
)
'''

JQUEUING_JOB_ACCOMPLISHED_LATENCY = 'jqueuing_job_accomplished_latency'
'''
Histogram(
    'jqueuing_job_accomplished_latency', 'jqueuing_job_accomplished_latency',
    ['node_id', 'qworker_id', 'job_id']
)
'''

def run_job(node_id, qworker_id, job_id):
	statsd.increment(JQUEUING_JOB_RUNNING_COUNT,
		tags=[
			'node_id:%s' % node_id,
			'qworker_id: %s' % qworker_id,
			'job_id: %s' % job_id,
		]
	)

def terminate_job(node_id, qworker_id, job_id, start_time):
	elapsed_time = time.time() - start_time
	statsd.histogram(JQUEUING_JOB_ACCOMPLISHED_LATENCY,
		elapsed_time,
		tags=[
			'node_id:%s' % node_id,
			'qworker_id: %s' % qworker_id,
			'job_id: %s' % job_id,
		]
	)
	statsd.increment(JQUEUING_JOB_ACCOMPLISHED_COUNT,
		tags=[
			'node_id:%s' % node_id,
			'qworker_id: %s' % qworker_id,
			'job_id: %s' % job_id,
		]
	)
	statsd.decrement(JQUEUING_JOB_RUNNING_COUNT,
		tags=[
			'node_id:%s' % node_id,
			'qworker_id: %s' % qworker_id,
			'job_id: %s' % job_id,
		]
	)

JQUEUING_TASK_RUNNING_COUNT = 'jqueuing_task_running_count'
'''
Gauge(
    'jqueuing_task_running_count', 'jqueuing_task_running_count',
    ['node_id', 'qworker_id', 'job_id', 'task_id']
)
'''

JQUEUING_TASK_ACCOMPLISHED_COUNT = 'jqueuing_task_accomplished_count'
'''
Counter(
    'jqueuing_task_accomplished_count', 'jqueuing_task_accomplished_count',
    ['node_id', 'qworker_id', 'job_id', 'task_id']
)
'''

JQUEUING_TASK_ACCOMPLISHED_LATENCY = 'jqueuing_task_accomplished_latency'
'''
Histogram(
    'jqueuing_task_accomplished_latency', 'jqueuing_task_accomplished_latency',
    ['node_id', 'qworker_id', 'job_id', 'task_id']
)
'''

def run_task(node_id, qworker_id, job_id, task_id):
	statsd.increment(JQUEUING_TASK_RUNNING_COUNT,
		tags=[
			'node_id:%s' % node_id,
			'qworker_id: %s' % qworker_id,
			'job_id: %s' % job_id,
			'task_id: %s' % task_id,
		]
	)

def terminate_task(node_id, qworker_id, job_id, task_id, start_time):
	elapsed_time = time.time() - start_time
	statsd.histogram(JQUEUING_TASK_ACCOMPLISHED_LATENCY,
		elapsed_time,
		tags=[
			'node_id:%s' % node_id,
			'qworker_id: %s' % qworker_id,
			'job_id: %s' % job_id,
			'task_id: %s' % task_id,
		]
	)
	statsd.increment(JQUEUING_TASK_ACCOMPLISHED_COUNT,
		tags=[
			'node_id:%s' % node_id,
			'qworker_id: %s' % qworker_id,
			'job_id: %s' % job_id,
			'task_id: %s' % task_id,
		]
	)
	statsd.decrement(JQUEUING_TASK_RUNNING_COUNT,
		tags=[
			'node_id:%s' % node_id,
			'qworker_id: %s' % qworker_id,
			'job_id: %s' % job_id,
			'task_id: %s' % task_id,
		]
	)
