#obs default 12/7/2017 by rqm
# greedy, send as many as it can
import math

fps = 30
T = 7500  #60s
GoP = 30 # 15~60 frames

Bitrate = 2850000 # bps, 2mbps
Bmax = 27 # frame
Frame = Bitrate//fps # each frame how much bps

def obs():
	array = [] # first, assume the array is empty
	input = open("trace.txt")
	output = open("obs-throughput.txt","w+")

	buf = open("obs-buffer.txt", "w+")

	buffer = 0.0
	remain = 0.0
	priority = False
	drop = 0
	Dropped = []
	throughput = []

	for time in range(T):
		if time%fps == 0:
			bandwidth = float(input.readline())*1000.0//fps

		inital = 0.0

		Drop_initial = drop

		if not priority:
			array.append(time)
			buffer = buffer + Frame
		else:
			if time%GoP == 0:
				array.append(time)
				buffer = buffer + Frame
				priority = False
			else:
				drop = drop + 1

		inital = buffer

		if remain<bandwidth and len(array):
			count = min(math.ceil((bandwidth-remain)/Frame), len(array))
			while count:
				first = array[0]
				array.remove(first)
				count = count - 1

		buffer = max(buffer - bandwidth, 0)

		throughput.append(inital - buffer)

		if len(array) and max(array)-min(array)+1>=Bmax:
			new_array = []
			delete = 0.0
			for num in array:
				if num%GoP==0:
					new_array.append(num)
				else:
					delete = delete+1
					drop = drop + 1
			buffer = max(buffer-delete*Frame, 0)
			array = new_array
			priority = True
		remain = buffer%Frame

		buf.write(str(buffer)+'\n')

		Dropped.append(drop - Drop_initial)


	print "Dropped Frames:"+str(drop)

	all = 0.0
	for item in range(len(throughput)):
		if item!=0 and item%30 == 0:
			output.write(str(all)+'\n')
			all = 0.0
		all = all + throughput[item]
	output.write(str(all)+'\n')

	all = 0
	info = open("obs-drop.txt", "w+")
	for item in range(len(Dropped)):
		if item%30==0:
			info.write(str(all)+'\n')
			all = 0

		all = all + Dropped[item]

	info.write(str(all)+'\n')


def main():
	obs()

if __name__=='__main__':
	main()