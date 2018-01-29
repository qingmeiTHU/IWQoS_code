# mpc, 12/27/2017 by rqm
# assume the buffer empty at first
import math

fps = 30
T = 9000  #300s
GoP = 30 # 15~60 frames

alpha = 0.5
tau = 5
beta = 1500

Bitrate = [350000, 600000, 1000000, 1500000, 2000000] #kbps, 350, 600, 1000, 1500, 2000
Bmax = 27 #frame

Max = -2147483648

def mpc_cal(Bandwidth, total, all, rate, buffer, remain, Send, Size, index, M, final_rate):
	if total==all:
		Num = 0
		drop = 0 
		for i in range(all): #choose the tau-th bitrate
			priority = False
			Frame = rate[i]//fps
			Num = Num + rate[i]/10000
			if i>=1:
				Num = Num - alpha*abs(rate[i]-rate[i-1])/10000

			for j in range(GoP):
				if priority:
					drop = drop + 1
				else:
					Send.append((i+index)*GoP+j)
					Size.append(Frame)
					buffer = buffer + Frame

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

		Num = Num - beta*drop
		if Num>M:
			M = Num
			final_rate = rate[0]
		return (final_rate,M)
	else:
		for i in range(5):
			rate.append(Bitrate[i])
			New_Send = Send[:]
			New_Size = Size[:]
			final_rate,M = mpc_cal(Bandwidth,total+1,all,rate,buffer,remain,New_Send,New_Size,index,M,final_rate)
			New_Send = Send[:]
			New_Size = Size[:]
			rate.pop()
		return (final_rate,M)

def mpc_optimal():
	input = open('trace.txt','r')
	output = open('mpc-optimal-throughput.txt','w+')
	buf = open('mpc-optimal-buffer.txt','w+')
	bt = open('mpc-optimal-bitrate.txt','w+')

	Bandwidth = []
	for index in range(T):
		if index%fps==0:
			real_bandwidth = float(input.readline())//fps
			Bandwidth.append(real_bandwidth)
		else:
			Bandwidth.append(real_bandwidth)

	remain = 0
	buffer = 0
	Send = []
	Size = []
	Bw_history = []
	priority = False
	drop = 0
	for index in range(T/GoP): #choice of bitrates
		final_rate = 0
		priority = False
		M = Max
		all = min(tau,T/GoP-index)
		predict_Bandwidth = Bandwidth[index*GoP:(index+all)*GoP]
		final_rate,M = mpc_cal(predict_Bandwidth,0,all,[],buffer,remain,Send,Size,index,M,final_rate)
		bt.write(str(final_rate)+'\n')

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
			buf.write(str(buffer)+'\n')
			
		output.write(str(throughput)+'\n')
		print drop, Send,Size,final_rate

def main():
	mpc_optimal()

if __name__ == '__main__':
	main()