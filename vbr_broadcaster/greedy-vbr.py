# oracle, 12/6/2017 rqm
# assume the buffer empty at first
import math
import os  

DATA_PATH = '../traces/all/'
OUTPUT_PATH = '../greedy-vbr/'
fps = 30
T = 9600  #60s
GoP = 30 # 15~60 frames

tau = 4
alpha = 0.08

beta = 5000
Bitrate = [300000,750000,1200000,1850000,2850000,4300000]
Bmax = 27 # frame

def predict_bandwidth(Bw_history, Error):
	Error = 0.0
	tmp = []
	count = 0
	for item in range(len(Bw_history)):
		if item%GoP==0:
			tmp.append(1.0/Bw_history[item]/30.0)
			count = count + 1
	average = count/sum(tmp) if len(Bw_history)>0 else 300000
	#average = sum(Bw_history)/len(Bw_history)*30.0 if len(Bw_history)>0 else 300000
	return average

def choose_bitrate(bandwidth):
	pre_rate = Bitrate[0]
	for rate in Bitrate:
		if rate>bandwidth:
			return pre_rate
		pre_rate = rate
	return Bitrate[-1]

def greedy():
	files = os.listdir(DATA_PATH)
	for file in files:
		#file = 'test_fcc_trace_1171_http---www.yahoo.com_0'
		file_path = DATA_PATH + file
		output_path = OUTPUT_PATH + file
		print file_path

		Bandwidth = []
		input = open(file_path,'r')
		#output = open("greedy-350-throughput.txt", "w+")
		bt = open(output_path+'-bitrate.txt','w+')
		dropped = open(output_path+'-dropped.txt','w+')

		for time in range(T):
			if time%fps==0:
				real_bandwidth = float(input.readline())*1000.0//fps
				Bandwidth.append(real_bandwidth)
			else:
				Bandwidth.append(real_bandwidth)

		priority = False

		drop = 0
		tmp = []
		remain = 0
		throughput = []
		buffer = 0
		Bw_history = []
		Buffer = []
		Size = []
		priority = False
		Error = 0.0
		Esm_history = []
		final_sum = 0.0
		pre_rate = 0.0
		smooth = 0.0

		for index in range(T/GoP):
			predict_Bandwidth = predict_bandwidth(Bw_history, Error)
			final_rate = choose_bitrate(predict_Bandwidth)
			Frame = final_rate//fps
			bt.write(str(final_rate)+'\n')
			for j in range(GoP):
				Esm_history.append(predict_Bandwidth)
			if index>=tau:
				Bw_history = Bandwidth[(index+1-tau)*GoP:(index+1)*GoP]
				for j in range(GoP):
					Esm_history.remove(Esm_history[0])
			else:
				Bw_history = Bandwidth[0:(index+1)*GoP]

			final_sum = final_sum + final_rate/10000.0/T*GoP
			if index>0:
				final_sum = final_sum - alpha*abs(final_rate-pre_rate)/10000.0/T*GoP
				smooth = smooth + abs(final_rate-pre_rate)

			Error = 0.0
			for j in range(len(Esm_history)):
				if j%GoP==0:
					Error = max(Error, abs(Esm_history[j]-Bw_history[j])/Bw_history[j])

			for i in range(GoP):
				Buffer.append(index*GoP+i)
				Size.append(Frame)
				buffer = buffer + Frame

				count = 0
				if priority: # drop the unencoded frames
					for block in range(len(Buffer)):
						if Buffer[block]%GoP == 0:
							priority = False
							break
						else:
							if priority:
								count = count + 1
								drop = drop + 1
								buffer = buffer - Size[block]

				Buffer = Buffer[count:]
				Size = Size[count:]

				if remain<Bandwidth[index*GoP+i]:
					rest = Bandwidth[index*GoP+i] - remain
					while len(Buffer) and rest>0:
						first = Buffer[0]
						Buffer.remove(first)
						rest = rest - Size[0]
						Size.remove(Size[0])
					if rest<0:
						remain = -rest
					else:
						remain = 0
				else:
					remain = remain - Bandwidth[i+index*GoP]

				buffer = max(buffer-Bandwidth[index*GoP+i], 0)

				if len(Buffer) and index*GoP+i - min(Buffer) + 1 >= Bmax: # dropped
					new_State = []
					new_Size = []
					for block in range(len(Buffer)):
						if index*GoP+i - Buffer[block] + 1 < Bmax:
							new_State.append(Buffer[block])
							new_Size.append(Size[block])
						else:
							priority = True
							drop = drop + 1
							buffer = buffer - Size[block]

					Buffer = new_State
					Size = new_Size
				pre_rate = final_rate

		final_sum = final_sum - drop*beta
		print drop
		dropped.write(str(drop)+' '+str(smooth*alpha/10000.0/T*GoP)+' '+str(final_sum))
		dropped.close()



def main():
	greedy()

if __name__ == '__main__':
	main()