import matplotlib.pyplot as plt
import numpy as np

trace = open("trace.txt")
obs_throughput = open("obs-throughput.txt")
greedy_throught = open("greedy-throughput.txt")
oracle_throughput = open("optimal-throughput.txt")

count = 0
x_trace = []
y_trace = []

for line in trace:
	count = count + 1
	y_trace.append(float(line))
	x_trace.append(count)

print len(y_trace)

count = 0
x_throughput = []
y_throughput = []
for line in obs_throughput:
	count = count + 1
	x_throughput.append(count)
	y_throughput.append(float(line))

count = 0
gx_throughput = []
gy_throught = []
for line in greedy_throught:
	count = count + 1
	gx_throughput.append(count)
	gy_throught.append(float(line))

count = 0
opx_throughput = []
opy_throughput = []
for line in oracle_throughput:
	count = count + 1
	opx_throughput.append(count)
	opy_throughput.append(float(line))

plt.plot(x_trace, np.array(y_trace)*1000)
plt.xlim(0,250)
#plt.ylim(0,30)
plt.plot(x_throughput, y_throughput,linestyle='--')
plt.plot(gx_throughput, gy_throught,linestyle='-')
plt.plot(opx_throughput, opy_throughput,linestyle='-.')
plt.ylabel("Bandwidth(bps)")
plt.xlabel("Time(S)")

#plt.xlim(0,)
plt.legend(labels=['trace','obs','greedy','optimal'])
plt.show()