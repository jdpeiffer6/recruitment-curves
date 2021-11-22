import numpy as np
import matplotlib.pyplot as plt
import glob

filez = glob.glob("output\\*data.npy")
# meta = glob.glob("*meta.npy")

mydata = np.load("output\\dummy_multithread_0_data.npy")
fig, axs = plt.subplots(mydata.shape[0], 1)
x=np.linspace(0,0.1,num=mydata.shape[1])

avgs = np.zeros(mydata.shape)

for file in filez:
    mydata = np.load(file)
    for i in range(mydata.shape[0]):
        axs[i].plot(x,mydata[i,:],alpha=0.6,color="#BFBFBF", lw=1.5)
        avgs[i,:] += mydata[i,:]

avgs = np.divide(avgs,len(filez))
for i in range(mydata.shape[0]):
    axs[i].plot(x, avgs[i,:], color="#0b53c1", lw=2.4, zorder=10)
    # axs[i].scatter(x, avgs[i,:], fc="w", ec="#0b53c1", s=60, lw=2.4, zorder=12) 

for i in range(len(axs)):
    axs[i].grid(True)


axs[0].set_title("Gastroc")
axs[1].set_title("TA")
plt.xlabel("Time (s)")
plt.show()

for file in filez:
    mydata = np.load(file)
    for i in range(mydata.shape[0]):
        plt.plot(x,mydata[i,:],alpha=0.6, lw=1.5)
        plt.show()
