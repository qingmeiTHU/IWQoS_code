# trace distribution
import os
import numpy as np
import matplotlib.pyplot as plt

INPUT_PATH = 'all/'
FCC_PATH = 'fcc/'
NOR_PATH = 'norway/'

all_bandwidth = []
fcc_bandwidth = []
nor_bandwidth = []

def cal():
	count = 0
	files = os.listdir(INPUT_PATH)
	for file in files:
		count = count + 1
		file_path = INPUT_PATH.strip() + file.strip()

		input = open(file_path,'r')

		Bandwidth = []
		for line in input:
			Bandwidth.append(float(line))

		average = sum(Bandwidth)/len(Bandwidth)

		tmp_count = 0

		for bw in Bandwidth:
			if bw<average:
				tmp_count = tmp_count + 1
			else:
				if tmp_count ==0:
					continue
				all_bandwidth.append(tmp_count)
				tmp_count = 0

	all_bandwidth.sort()
	#print all_bandwidth
	all_cdf = np.arange(len(all_bandwidth))/float(len(all_bandwidth)-0.0001)
	plt.plot(all_bandwidth,all_cdf,label='all-traces',linestyle='--',linewidth=4)
	#plt.plot([0,0],[0,1],'r', linestyle='--')

	files = os.listdir(FCC_PATH)
	for file in files:
		file_path = FCC_PATH.strip() + file.strip()

		input = open(file_path,'r')

		Bandwidth = []
		for line in input:
			Bandwidth.append(float(line))

		average = sum(Bandwidth)/len(Bandwidth)

		tmp_count = 0

		for bw in Bandwidth:
			if bw<average:
				tmp_count = tmp_count + 1
			else:
				if tmp_count ==0:
					continue
				fcc_bandwidth.append(tmp_count)
				tmp_count = 0
	fcc_bandwidth.sort()
	fcc_cdf = np.arange(len(fcc_bandwidth))/float(len(fcc_bandwidth)-0.0001)
	plt.plot(fcc_bandwidth,fcc_cdf, label='fcc', linestyle='-.',linewidth=4)	

	files = os.listdir(NOR_PATH)
	for file in files:
		file_path = NOR_PATH.strip() + file.strip()

		input = open(file_path,'r')

		Bandwidth = []
		for line in input:
			Bandwidth.append(float(line))

		average = sum(Bandwidth)/len(Bandwidth)

		tmp_count = 0

		for bw in Bandwidth:
			if bw<average:
				tmp_count = tmp_count + 1
			else:
				if tmp_count ==0:
					continue
				nor_bandwidth.append(tmp_count)
				tmp_count = 0

	nor_bandwidth.sort()
	nor_cdf = np.arange(len(nor_bandwidth))/float(len(nor_bandwidth)-0.0001)
	plt.plot(nor_bandwidth,nor_cdf, label='norway',linewidth=4)	
	plt.legend(fontsize=16)
	plt.ylim(0,1)
	#plt.xlim(-1,4)
	plt.xlabel('Banwidth Down Seconds',fontsize=16)
	plt.ylabel('CDF',fontsize=16)
	plt.yticks(fontsize=16)
	plt.xticks(fontsize=16)
	plt.show()


def main():
	cal()

if __name__ == '__main__':
	main()