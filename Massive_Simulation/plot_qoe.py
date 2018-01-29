import matplotlib.pyplot as plt
import numpy as np

N = 4
result = [-3921463.54945,-596392.394836,-338191.380835,-340722.065166]

normal_result = abs((np.array(result) - min(result))/min(result)) + 1.0

index = 0.5
bar_width = 0.5

plt.bar(index, normal_result[0], bar_width, label='obs-cbr')
plt.bar(index+1, normal_result[1], bar_width, label='obs-vbr')
plt.bar(index+2, normal_result[2], bar_width, label='mpc')
plt.bar(index+3, normal_result[3], bar_width, label='greedy-vbr')

plt.xlabel('Algorithms')
plt.ylabel('Normalized QoE')

plt.xticks([])
plt.legend()
plt.show()