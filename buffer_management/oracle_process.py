file = open("all_possible_method.txt")
input = open("all_posible_throughput.txt")

Record = []
for line in file:
	string=line.strip().split('\t')
	Record.append(string)

th_record = []
for line in input:
	string = line.strip().split('\t')
	th_record.append(string)

Result = []
buf = []
throughput = []

i=929
index = 0
while i>=0:
	real_buffer = Record[i][index].split(')')[1].split(',')[1]
	real_throughput = th_record[i][index]
	throughput.append(real_throughput)
	buf.append(float(real_buffer))
	Result.append(Record[i][index])
	right = Record[i][index]
	index = int(right.split(':')[1])
	i = i - 1

#print Result
Result.reverse()
buf.reverse()
throughput.reverse()

buf_out = open("optimal-buffer.txt","w")
th_out = open('optimal-throughput.txt','w')

total = 0
for i in range(len(throughput)):
	#print str(buf)
	buf_out.write(str(buf[i])+'\n')
	if i%30==0 and i!=0:
		th_out.write(str(total)+'\n')
		total = float(throughput[i])
	else:
		total = total + float(throughput[i])
th_out.write(str(total)+'\n')

buf_out.close()
th_out.close()