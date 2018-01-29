import matplotlib.pyplot as plt

obs_buf = open("obs-buffer.txt")
oracle_buf = open("oracle-buffer.txt")

count = 0
obs_x = []
obs_y = []
for line in obs_buf:
	count = count + 1
	obs_y.append(float(line))
	obs_x.append(count)

count = 0
oracle_x = []
oracle_y = []
for line in oracle_buf:
	count = count + 1
	oracle_x.append(count)
	oracle_y.append(float(line))

plt.plot(obs_x, obs_y)
plt.plot(oracle_x, oracle_y)

plt.show()