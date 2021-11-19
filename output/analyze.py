import numpy as np
import matplotlib.pyplot as plt


# mydata = np.load("output\\myfile.npy")
mydata = np.load("output\\dummy_multithread.npy")
# for i in range(mydata.shape[1]):
#     if mydata[0,i]>500 or mydata[1,i]>500 or mydata[0,i]<500 or mydata[1,i]<500:
#         mydata[:,i]=0
x=np.linspace(0,5,num=mydata.shape[1])
for i in range(mydata.shape[0]):
    plt.plot(x,mydata[i,:],alpha=0.6)

plt.xlabel("Time (s)")
plt.show()

