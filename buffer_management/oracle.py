#oracle 12/12/2017 by rqm
# dynamic programming
import math
import copy

fps = 30 # produce 30 frames each second
T = 930  #180s 30*180=1800
GoP = 30 # 15~60 frames

Bitrate = 2850000 # 1.5mbps, 2mbps
Bmax = 27 # frame
Bool = [False, True]
Default = 274# the greedy limit
Frame_Size = Bitrate//fps
# dynamic program, just decide drop the frame or not
# send as much as possible chunks when avaliable
output = open("optimal-buffer.txt", "w")

Record = dict()
throughput = dict()

def traversal(item, index, count, front, Frame, buffer, remain, drop, dic, priority, send):
	if index<=count:#Frame backup
		Size = len(Frame)
		back = []
		for i in range(Size):
			if i!=0 and Frame[i]%GoP==0:#
				back = Frame[i:] 
				break	
			front.append(Frame[i])

		Size = len(front)
		for i in range(Size+1):
			New_front = front[:i]
			New_drop = drop + Size - i
			New_buffer = buffer - Size*Frame_Size + i*Frame_Size
			New_priority = priority
			if len(back)==0 and i!=Size:
				New_priority = True
			dic2 = traversal(item, index+1, count, New_front, back, New_buffer, remain, New_drop, dic, New_priority, send)
			dicMerged = dic.copy()
			dicMerged.update(dic2)
			dic = dicMerged.copy()
	else:
		Tuple = (tuple(front+Frame), buffer, remain, priority)
		#print Tuple]
		From = item
		if dic.has_key(Tuple):
			From = (Record[Tuple] if dic[Tuple]<drop else item)
			send = (throughput[Tuple] if dic[Tuple]<drop else send)
			drop = min(dic[Tuple], drop)

		dic[Tuple] = drop
		Record[Tuple] = From
		throughput[Tuple] = send

	return dic

def optimal():
	input = open('test_fcc_trace_10652_http---www.amazon.com_1020', 'r')
	output = open("all_possible_method.txt", "w+")
	through = open("all_posible_throughput.txt", "w+")

	buffer = 0 
	MIN = 0

	for index in range(T):#T time slot
		dic = dict()
		Record.clear()
		throughput.clear()

		if index%fps == 0:
			bandwidth = float(input.readline())*1000.0//fps

		if index == 0:#the first block
			buffer = buffer + Frame_Size
			priority = False
			remain = 0
			drop = 0
			Frame = (1,)
			if bandwidth==0:
				for i in range(2):#drop or not
					drop = i
					priority = Bool[i]
					New_buffer = buffer - i*Frame_Size
					if i==1:
						Frame = ()
					Tuple = (Frame, New_buffer, remain, priority)
					dic[Tuple] = drop
					Record[Tuple] = 0
					throughput[Tuple] = 0
			else: #buffer has no more chunk left
				Frame = () #no keyframe in buffer
				remain = max(0, Frame_Size-bandwidth)
				buffer = remain
				Tuple = (Frame, buffer, remain, priority)
				dic[Tuple] = drop
				Record[Tuple] = 0
				throughput[Tuple] = Frame_Size-buffer
		else:
			for item in range(len(State)): # the previous state
				Frame = list(State[item][0])
				drop = State[item][4]
				if (len(Frame)==0 or index-min(Frame)+1<Bmax) and drop<=Default:#if exceed the limit, abandon
					buffer = State[item][1]
					priority = State[item][3]
					if priority==False or (index+1)%GoP==0: # another key frame arrived
						buffer = buffer + Frame_Size
						Frame.append(index+1)
						priority = False 
					else:
						drop = drop + 1

					remain = State[item][2]

					initial = buffer

					if remain<bandwidth and buffer-remain > 0:# send as many as frames
						count = min(math.ceil((bandwidth - remain)/Frame_Size), len(Frame))
						while count:
							first = Frame[0]
							Frame.remove(first)
							count = count - 1 # buffer or bandwidth

					buffer = max(buffer-bandwidth,0)
					send = initial-buffer
					remain = buffer%Frame_Size

					if len(Frame)>0:# each possible drop
						count = 0
						for i in range(len(Frame)):
							if Frame[i]%GoP ==0:
								count = count + 1
						(dic2) = traversal(item, 0, count, [], Frame, buffer, remain, drop, dic, priority, send)
						dic1=dic.copy()
						dic1.update(dic2)
						dic = dic1.copy()
					else:
						From = item
						Tuple = ((), buffer, remain, priority)
						if dic.has_key(Tuple):
							From = (Record[Tuple] if dic[Tuple]<drop else item)
							drop = min(dic[Tuple], drop)
							send = (throughput[Tuple] if dic[Tuple]<drop else send)
						dic[Tuple] = drop
						Record[Tuple] = From
						throughput[Tuple] = send


		State = []
		MIN = T
		for key, value in dic.items():
			output.write(str(key)+':'+str(Record[key])+'\t')
			through.write(str(throughput[key])+'\t')
			key = key + (value,)
			State.append(key)
			MIN = min(MIN, value)
		output.write('\n')
		through.write('\n')
		print index, len(State)
	print "dropped frames:",MIN


def main():
	optimal()

if __name__ == '__main__':
	main()