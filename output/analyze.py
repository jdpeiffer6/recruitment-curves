import numpy as np
import matplotlib.pyplot as plt


mydata = np.load("output\\myfile.npy")
# for i in range(mydata.shape[1]):
#     if mydata[0,i]>500 or mydata[1,i]>500 or mydata[0,i]<500 or mydata[1,i]<500:
#         mydata[:,i]=0

plt.plot(mydata[0,:],alpha=0.6)
plt.plot(mydata[1,:],alpha=0.6)
plt.show()

