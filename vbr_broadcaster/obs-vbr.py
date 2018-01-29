#obs default 12/7/2017 by rqm
# greedy, send as many as it can
import math
import os  

DATA_PATH = '../traces/all/'
OUTPUT_PATH = '../obs-vbr/'

beta = 5000
tau = 4
alpha = 0.08

fps = 30
T = 9600  #60s
GoP = 30 # 15~60 frames
Bitrate = [300000,750000,1200000,1850000,2850000,4300000]
Bmax = 27 # frame

def predict_bandwidth(Bw_history):
	tmp = []
	count = 0
	for item in range(len(Bw_history)):
		if item%GoP==0:
			tmp.append(1.0/Bw_history[item]/30.0)
			count = count + 1
	average = count/sum(tmp) if len(Bw_history)>0 else 300000
	return average

def choose_bitrate(bandwidth):
	pre_rate = Bitrate[0]
	for rate in Bitrate:
		if rate>bandwidth:
			return pre_rate
		pre_rate = rate
	return Bitrate[-1]

def obs():
	files = os.listdir(DATA_PATH)
	for file in files:
		#file = 'test_fcc_trace_1171_http---www.yahoo.com_0'
		file_path = DATA_PATH + file
		output_path = OUTPUT_PATH + file
		print file_path

		dropped = open(output_path+'-dropped.txt','w+')
		bt = open(output_path+'-bitrate.txt','w+')
		input = open(file_path,'r')

		Bandwidth = []
		for time in range(T):
			if time%fps==0:
				real_bandwidth = float(input.readline())*1000.0//fps
				Bandwidth.append(real_bandwidth)
			else:
				Bandwidth.append(real_bandwidth)

		buffer = 0.0
		remain = 0.0
		priority = False
		drop = 0
		Size = []
		Bw_history = []
		Buffer = [] # first, assume the array is empty
		pre_rate = 0.0
		final_sum = 0.0
		smooth = 0.0

		for time in range(T/GoP):
			predict_Bandwidth = predict_bandwidth(Bw_history)
			final_rate = choose_bitrate(predict_Bandwidth)
			Frame = final_rate//fps
			bt.write(str(final_rate)+'\n')
			
			final_sum = final_sum + final_rate/10000.0/T*GoP
			if time>0:
				final_sum = final_sum - alpha*abs(final_rate-pre_rate)/10000.0/T*GoP
				smooth = abs(final_rate-pre_rate) + smooth

			if time>=tau:
				Bw_history = Bandwidth[(time+1-tau)*GoP:(time+1)*GoP]
			else:
				Bw_history = Bandwidth[0:(time+1)*GoP]

			for i in range(GoP):
				bandwidth = Bandwidth[time*GoP+i]
				if not priority:
					Buffer.append(time*GoP+i)
					Size.append(Frame)
					buffer = buffer + Frame
				else:
					if i == 0:
						Buffer.append(time*GoP+i)
						buffer = buffer + Frame
						Size.append(Frame)
						priority = False
					else:
						drop = drop + 1

				if remain<bandwidth and len(Buffer):
					rest = bandwidth - remain
					while len(Buffer) and rest>0:
						rest = rest - Size[0]
						Buffer.remove(Buffer[0])
						Size.remove(Size[0])
					if rest<0:
						remain = -rest
					else:
						remain = 0
				else:
					remain = remain - bandwidth

				buffer = max(buffer - bandwidth, 0)

				if len(Buffer) and time*GoP+i-min(Buffer)+1>=Bmax:
					new_Buffer = []
					new_Size = []
					for num in range(len(Buffer)):
						if Buffer[num]%GoP==0:
							new_Buffer.append(Buffer[num])
							new_Size.append(Size[num])
						else:
							drop = drop + 1
							priority = True
							buffer = buffer - Size[num]
					Buffer = new_Buffer
					Size = new_Size
			pre_rate = final_rate
		print drop
		final_sum = final_sum - drop*beta
		dropped.write(str(drop)+' '+str(smooth*alpha/10000.0/T*GoP)+' '+str(final_sum))
		dropped.close()

def main():
	obs()

if __name__=='__main__':
	main()