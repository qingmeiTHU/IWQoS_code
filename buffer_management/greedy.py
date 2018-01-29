# oracle, 12/6/2017 rqm
# assume the buffer empty at first
import math

fps = 30
T = 7500  #60s
GoP = 30 # 15~60 frames

Bitrate = 2850000 # kbps, 2mbps
Bmax = 27 # frame
Frame = Bitrate//fps # kbps

def greedy():
	input = open('trace.txt','r')
	output = open("greedy-throughput.txt", "w+")
	buf = open("greedy-buffer.txt", "w+")

	priority = False
	State = [[] for i in range(T)] # each time slot, state contains the first keyframe, remain and priority

	drop = 0
	tmp = []
	remain = 0
	throughput = []
	buffer = 0

	for index in range(T):
		if index%fps == 0:
			bandwidth = float(input.readline())*1000.0//fps

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
		buf.write(str(buffer)+'\n')

	all = 0
	for item in range(len(throughput)):
		if item!=0 and item%30 == 0:
			output.write(str(all)+'\n')
			all = 0.0
		all = all + throughput[item]
	output.write(str(all)+'\n')

	print "Dropped Frames:"+ str(drop)


def main():
	greedy()

if __name__ == '__main__':
	main()