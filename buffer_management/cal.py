input = open('trace.txt','r')
output = open('real-trace.txt','wb')

for line in input:
	output.write(str(int(float(line.strip())*1000))+'\n')