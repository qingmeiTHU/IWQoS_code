import matplotlib.pyplot as plt
import numpy as np

N = 4
result = [784.314285714/30.0,119.298901099/30.0,67.6593406593/30.0,68.1648351648/30.0]

index = 0.5
bar_width = 0.5

plt.bar(index, result[0], bar_width, label='greedy')
plt.bar(index+1, result[1], bar_width, label='obs-vbr')
plt.bar(index+2, result[2], bar_width, label='mpc')
plt.bar(index+3, result[3], bar_width, label='greedy-vbr')

plt.xlabel('Algorithms')
plt.ylabel('Black Screen Seconds')
#plt.yscale("log")

plt.xticks([])
plt.legend()
plt.show() 