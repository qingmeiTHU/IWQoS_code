import math
import os

MPC_PATH = '../mpc/'
TRACE_PATH = '../traces/'

files = os.listdir(MPC_PATH)

total = []

for file in files:
	Bitrate = []

	if '-dropped.txt' in file:
		nPos = file.index('-dropped')
		tracename = file[:nPos]
		tracepath = TRACE_PATH + tracename
		filepath = MPC_PATH + file

		bitratepath = MPC_PATH + tracename + '-bitrate.txt'

		input = open(filepath,'r')
		trace = open(tracepath, 'r')
		bitrate = open(bitratepath, 'r')

		all = 0.0
		for line in trace:
			all = all + float(line)*1000.0

		tmp = 0.0
		for line in bitrate:
			tmp = tmp + float(line)

		average = tmp/320

		for line in input:
			drop = float(line.strip().split(' ')[0])

		tmp = tmp - drop/30.0*average

		total.append(tmp/all)

print sum(total)/len(total)