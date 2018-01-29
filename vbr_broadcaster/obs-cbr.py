# oracle, 12/6/2017 rqm
# assume the buffer empty at first
import math
import os  

DATA_PATH = '../traces/all/'
OUTPUT_PATH = '../obs-cbr/'
fps = 30
T = 9600  #60s
GoP = 30 # 15~60 frames

beta = 5000
Bitrate = [300000,750000,1200000,1850000,2850000,4300000]
Bmax = 27 # frame

def find_rate(bandwidth):
	prepre_rate = Bitrate[0]
	pre_rate = Bitrate[0]
	for rate in Bitrate:
		if rate>bandwidth:
			return pre_rate
		pre_rate = rate
	return Bitrate[-1]

def greedy():
	files = os.listdir(DATA_PATH)
	for file in files:
		file_path = DATA_PATH + file
		output_path = OUTPUT_PATH + file
		print file_path

		Bandwidth = []
		input = open(file_path,'r')
		dropped = open(output_path+'-dropped.txt','w+')

		for time in range(T/GoP):
			Bandwidth.append(float(input.readline())*1000.0)

		estimate_bandwidth = sum(Bandwidth)/len(Bandwidth)
		final_rate = find_rate(estimate_bandwidth)
		Frame = final_rate//fps
		priority = False
		State = [[] for i in range(T)] # each time slot, state contains the first keyframe, remain and priority

		drop = 0
		tmp = []
		remain = 0
		throughput = []
		buffer = 0

		for index in range(T):
			bandwidth = Bandwidth[index/GoP]//fps

			State[index] = tmp
			State[index].append(index)
			buffer = buffer + Frame
			
			count = 0

			if priority: # drop the unencoded frames
				for block in State[index]:
					if block%GoP == 0:
						priority = False
						break
					else:
						if priority:
							count = count + 1
							drop = drop + 1
							buffer = buffer - Frame

			State[index] = State[index][count:]

			inital = buffer

			if remain<bandwidth and len(State[index]):
				count = min(math.ceil((bandwidth-remain)/Frame), len(State[index]))
				while count:
					first = State[index][0]
					State[index].remove(first)
					count = count - 1

			buffer = max(buffer-bandwidth, 0)
			throughput.append(inital-buffer)

			if len(State[index]) and index - min(State[index]) + 1 >= Bmax: # dropped
				new_State = []
				for block in State[index]:
					if index - block + 1 < Bmax:
						new_State.append(block)
					else:
						priority = True
						drop = drop + 1
						buffer = buffer - Frame

				State[index] = new_State

			remain = buffer%Frame

			tmp = State[index]
		final_sum = final_rate/10000.0 - drop*beta

		dropped.write(str(drop)+' '+str(final_rate)+' '+str(final_sum))
		dropped.close()



def main():
	greedy()

if __name__ == '__main__':
	main()