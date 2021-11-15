import numpy as np
import matplotlib.pyplot as plt


data = np.load("output\myfile.npy")
plt.plot(data[0,:],alpha=0.6)
plt.plot(data[1,:],alpha=0.6)
plt.show()

