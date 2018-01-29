import matplotlib.pyplot as plt
import numpy as np

N = 4

bitrate = [1078791.20879/1000000.0,1025577.26648/1000000.0,1078173.07692/1000000.0,1025577.26648/1000000.0]
drop = [784.314285714/30.0,119.298901099/30.0,67.6593406593/30.0,68.1648351648/30.0]
qoe = [-3921463.54945,-596392.394836,-338191.380835,-340722.065166]

bitrate = (np.array(bitrate)-min(bitrate))/min(bitrate) + 1.0
drop = (np.array(drop)-23)/23 + 1.0
qoe = (np.array(qoe)-min(qoe))/min(qoe) + 1.0

obs_cbr = [bitrate[0],drop[0],qoe[0]]
obs_vbr = [bitrate[1],drop[1],qoe[1]]
mpc = [bitrate[2], drop[2], qoe[2]]
greedy_vbr = [bitrate[3],drop[3],qoe[3]]

index = np.arange(0,7.5,2.5)
bar_width = 0.5

plt.bar(index, obs_cbr, bar_width, label='obs-cbr')
plt.bar(index+bar_width, obs_vbr, bar_width, label='obs-vbr')
plt.bar(index+2*bar_width, mpc, bar_width, label='mpc')
plt.bar(index+3*bar_width, greedy_vbr, bar_width, label='greedy-vbr')


plt.xticks(index+0.7,('Bitrate', 'Black Screen', 'QoE'), fontsize=12)
plt.yticks(fontsize=12)
plt.legend(fontsize=12)
plt.show()