# mpc, 12/27/2017 by rqm
# assume the buffer empty at first
import math
import os
import numpy as np
import multiprocessing

DATA_PATH = '../traces/all/'
OUTPUT_PATH = '../mpc/'

fps = 30
T = 9600  #60s
GoP = 30 # 15~60 frames

alpha = 0.08
tau = 4
beta = 5000

Bitrate = [300000,750000,1200000,1850000,2850000,4300000] #kbps, 350, 600, 1000, 1500, 2000
Bmax = 27#frame

Max = -2147483648

def predict_bandwidth(Bw_history, Error):
	#Error = 0.0
	predict_Bandwidth =[]
	Bw_tmp = Bw_history 
	for i in range(tau):
		tmp = []
		count = 0
		for item in range(len(Bw_tmp)):
			if item%GoP==0:
				tmp.append(1.0/Bw_tmp[item])
				count = count + 1
		average = count/sum(tmp) if len(Bw_tmp)>0 else 300000//fps

		for j in range(GoP):
			predict_Bandwidth.append(average/(1+Error))

		if len(Bw_tmp)==tau*GoP:
			for i in range(GoP):
				Bw_tmp.append(average)
				Bw_tmp.remove(Bw_tmp[0])
		else:
			for i in range(GoP):
				Bw_tmp.append(average)

	return predict_Bandwidth


def mpc_cal(Bandwidth, total, rate, buffer, remain, Send, Size, index, M, final_rate):
	if total==tau:
		Num = 0
		drop = 0
		'''if rate[0]==300000 and rate[1]==300000 and rate[2]==300000 and rate[3]==300000 and index==284:
			print Send, Size'''

		for i in range(tau): #choose the tau-th bitrate
			priority = False
			Frame = rate[i]//fps
			Num = Num + rate[i]/10000.0/tau
			if i>=1:
				Num = Num - alpha*abs(rate[i]-rate[i-1])/10000.0/tau

			for j in range(GoP):
				if priority:
					drop = drop + 1
				else:
					Send.append((i+index)*GoP+j)
					Size.append(Frame)
					buffer = buffer + Frame

				'''if rate[0]==300000 and rate[1]==300000 and rate[2]==300000 and rate[3]==300000 and index==284:
					print "Second "+str(j), drop, Send, Size, Bandwidth[j+i*GoP]'''
				if remain<Bandwidth[j+i*GoP]:
					rest = Bandwidth[j+i*GoP] - remain
					while len(Send) and rest>0:
						first = Send[0]
						Send.remove(first)
						rest = rest - Size[0]
						Size.remove(Size[0])
					if rest<0:
						remain = -rest
					else:
						remain = 0
				else:
					remain = remain - Bandwidth[j+i*GoP]
				'''if rate[0]==300000 and rate[1]==300000 and rate[2]==300000 and rate[3]==300000 and index==284:
					print "Second "+str(j), Send, Size'''

				buffer = max(buffer-Bandwidth[j+i*GoP],0)

				if len(Send) and GoP*(index+i)+j- min(Send)+1>=Bmax:
					new_Send = []
					new_Size = []
					for block in range(len(Send)):
						if GoP*(index+i)+j- Send[block] +1 < Bmax:
							new_Send.append(Send[block])
							new_Size.append(Size[block])
						else:
							priority = True
							drop = drop + 1
							buffer = buffer - Size[block]
					Send = new_Send
					Size = new_Size

				'''if rate[0]==300000 and rate[1]==300000 and rate[2]==300000 and rate[3]==300000 and index==284:
					print "Second "+str(j), Send, Size'''

				count=0
				if priority:
					for block in range(len(Send)):
						if Send[block]%GoP==0:
							priority=False
							break
						else:
							if priority:
								count = count + 1
								drop = drop + 1
								buffer = buffer - Size[block]
				Send = Send[count:]
				Size = Size[count:]

				'''if rate[0]==300000 and rate[1]==300000 and rate[2]==300000 and rate[3]==300000 and index==284:
					print "Second "+str(j), Send, Size, drop'''

		Num = Num - beta*drop
		if Num>M:
			M = Num
			final_rate = rate[0]
		return (final_rate,M)
	else:
		for i in range(len(Bitrate)):
			rate.append(Bitrate[i])
			New_Send = Send[:]
			New_Size = Size[:]
			final_rate,M = mpc_cal(Bandwidth,total+1,rate,buffer,remain,New_Send,New_Size,index,M,final_rate)
			New_Send = Send[:]
			New_Size = Size[:]
			rate.pop()
		return (final_rate,M)


def single_job(file):
	final_sum = 0
	file_path = DATA_PATH + file
	output_path = OUTPUT_PATH + file
	smooth = 0.0

	input = open(file_path,'r') 
	dropped = open(output_path+'-dropped.txt','w+')
	bt = open(output_path+'-bitrate.txt','w+')

	estimate = open(output_path+'-estimate.txt','w+')

	Bandwidth = []
	for index in range(T):
		if index%fps==0:
			real_bandwidth = float(input.readline())*1000.0//fps
			Bandwidth.append(real_bandwidth)
		else:
			Bandwidth.append(real_bandwidth)

	Error = 0.0
	remain = 0
	buffer = 0
	Send = []
	Size = []
	Bw_history = []
	Esm_history = []
	priority = False
	drop = 0
	pre_rate = 0

	for index in range(T/GoP): #choice of bitrates
		final_rate = 0
		priority = False
		predict_Bandwidth = predict_bandwidth(Bw_history, Error)
		for j in range(GoP):
			Esm_history.append(predict_Bandwidth[0])
		if index >= tau:
			Bw_history = Bandwidth[(index+1-tau)*GoP:(index+1)*GoP]
			for j in range(GoP):
				Esm_history.remove(Esm_history[0])
		else:
			Bw_history = Bandwidth[0:(index+1)*GoP]

		estimate.write(str(predict_Bandwidth[0])+'\n')
		Error = 0.0
		for j in range(len(Esm_history)):
			if j%GoP==0:
				Error = max(Error, abs(Esm_history[j]-Bw_history[j])/Bw_history[j])

		M = Max
		final_rate,M = mpc_cal(predict_Bandwidth,0,[],buffer,remain,Send,Size,index,M,final_rate)
		'''if index==284:
			print np.array(predict_Bandwidth)*30
			print final_rate'''

		bt.write(str(final_rate)+'\n')
		final_sum = final_sum + final_rate/10000.0/T*GoP
		if index>0:
			final_sum = final_sum - alpha*abs(final_rate-pre_rate)/10000.0/T*GoP
			smooth = smooth + abs(final_rate-pre_rate)

		throughput = 0

		Frame = final_rate//fps
		for i in range(GoP):
			if priority:
				drop = drop + 1
			else:
				Send.append(i+index*GoP)
				Size.append(Frame)
				buffer = buffer + Frame

			initial = buffer

			if remain<Bandwidth[i+index*GoP]:
				rest = Bandwidth[i+index*GoP] - remain
				while len(Send) and rest>0:
					first = Send[0]
					Send.remove(first)
					rest = rest - Size[0]
					Size.remove(Size[0])
				if rest<0:
					remain = -rest
				else:
					remain = 0
			else:
				remain = remain - Bandwidth[i+index*GoP]

			buffer = max(buffer-Bandwidth[i+index*GoP],0)
			
			throughput = throughput + initial - buffer

			if len(Send) and GoP*index+i- min(Send)+1>=Bmax:
				new_Send = []
				new_Size = []
				for block in range(len(Send)):
					if GoP*index+i- Send[block] +1 < Bmax:
						new_Send.append(Send[block])
						new_Size.append(Size[block])
					else:
						priority = True
						drop = drop + 1
						buffer = buffer - Size[block]
				Send = new_Send
				Size = new_Size

			count=0
			if priority:
				for block in range(len(Send)): 
					if Send[block]%GoP==0:
						priority=False
						break
					else:
						if priority:
							count = count + 1
							drop = drop + 1
							buffer = buffer - Size[block]
			Send = Send[count:]
			Size = Size[count:]
		pre_rate = final_rate
	print drop
	final_sum = final_sum - beta*drop
	dropped.write(str(drop)+' '+str(smooth/10000.0/T*GoP)+' '+str(final_sum)+'\n')
	dropped.close()


def mpc():
	files = os.listdir(DATA_PATH)
	pool = multiprocessing.Pool(processes = 6)
	for index in xrange(len(files)):
		file = files[index]
		pool.apply_async(single_job, (file,)) 

	pool.close()
	pool.join()
	print 'done'

def main():
	mpc()

if __name__ == '__main__':
	main()