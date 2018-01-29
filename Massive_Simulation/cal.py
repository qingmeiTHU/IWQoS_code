import math
import os
import numpy as np

MPC_PATH = '../mpc/'

files = os.listdir(MPC_PATH)
Drop = []
total = []

for file in files:
	if '-dropped.txt' in file:
		Drop = []
		filepath = MPC_PATH + file
		input = open(filepath,'r')
		for line in input:
			drop = float(line.strip().split(' ')[2])
			Drop.append(drop)
		total.append(sum(Drop)/len(Drop))
		#print drop, fil1
#print sum(total)/len(total)

total.sort()
print total