import sys

params = sys.argv[1]
with open("./log", "a") as myfile:
	myfile.write(params + "\n")
print(params)
sys.exit(0)