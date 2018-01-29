import matplotlib.pyplot as plt

trace = open("../trace/fcc/test_norway_tram.ljabru-jernbanetorget-report.2011-01-31_2032CET.log")
greedy_1500_throught = open("greedy-1500-throughput.txt")
optimal_throughput = open("mpc-optimal-bitrate.txt")
mpc_throughput = open("mpc-bitrate.txt")
greedy_350_throught = open("greedy-350-throughput.txt")
greedy_2000_throught = open("greedy-2000-throughput.txt")

count = 0
gx_2000_throughput = []
gy_2000_throught = []
for line in greedy_2000_throught:
	count = count + 1
	gx_2000_throughput.append(count)
	gy_2000_throught.append(float(line))


count = 0
gx_350_throughput = []
gy_350_throught = []
for line in greedy_350_throught:
	count = count + 1
	gx_350_throughput.append(count)
	gy_350_throught.append(float(line))


count = 0
x_trace = [] 
y_trace = []
for line in trace:
	count = count + 1
	y_trace.append(float(line))
	x_trace.append(count)

count = 0
gx_1500_throughput = []
gy_1500_throught = []
for line in greedy_1500_throught:
	count = count + 1
	gx_1500_throughput.append(count)
	gy_1500_throught.append(float(line))

count = 0
opx_throughput = []
opy_throughput = []
for line in optimal_throughput:
	count = count + 1
	opx_throughput.append(count)
	opy_throughput.append(float(line))

count = 0
mpx_throughput = []
mpy_throughput = []
for line in mpc_throughput:
	count = count + 1
	mpx_throughput.append(count)
	mpy_throughput.append(float(line))

plt.plot(x_trace, y_trace)
#plt.plot(gx_350_throughput, gy_350_throught)
#plt.plot(gx_1500_throughput, gy_1500_throught)
#plt.plot(gx_2000_throughput, gy_2000_throught)
plt.plot(mpx_throughput, mpy_throughput)
#plt.plot(opx_throughput, opy_throughput)

plt.legend(labels=['trace','mpc','mpc-optimal'])
plt.show()