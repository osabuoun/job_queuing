import sys, time, random

from experiment_manager import add  

if __name__ == '__main__':
	experiment_id = "exp_" + str(int(round(time.time() * 1000))) + "_" + str(random.randrange(100, 999))
	service_name = str(sys.argv[1]) 
	experiment_params = sys.argv[2:]
	print("experiment_id:" + str(experiment_id))
	print("service_id:" + str(service_name))
	print("experiment_params:" + str(experiment_params))
	add.delay(
		experiment_id, 
		service_name, 
		experiment_params
	) 