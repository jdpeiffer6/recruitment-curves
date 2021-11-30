# import numpy as np
# import matplotlib.pyplot as plt
# import glob

# filez = glob.glob("output\\*data.npy")
# # meta = glob.glob("*meta.npy")

# mydata = np.load("output\\dummy_multithread_0_data.npy")
# fig, axs = plt.subplots(mydata.shape[0], 1)
# x=np.linspace(0,0.1,num=mydata.shape[1])

# avgs = np.zeros(mydata.shape)

# for file in filez:
#     mydata = np.load(file)
#     # mystim = np.load("output\\dummy_multithread_"+file[25]+"_stim.npy")
#     for i in range(mydata.shape[0]):
#         axs[i].plot(x,mydata[i,:],alpha=0.6,color="#BFBFBF", lw=1.5)
#         avgs[i,:] += mydata[i,:]

# avgs = np.divide(avgs,len(filez))
# for i in range(mydata.shape[0]):
#     axs[i].plot(x, avgs[i,:], color="#0b53c1", lw=2.4, zorder=10)
#     # axs[i].scatter(x, avgs[i,:], fc="w", ec="#0b53c1", s=60, lw=2.4, zorder=12) 

# for i in range(len(axs)):
#     axs[i].grid(True)


# axs[0].set_title("Gastroc")
# axs[1].set_title("TA")
# plt.xlabel("Time (s)")
# plt.show()

# for file in filez:
#     mydata = np.load(file)
#     for i in range(mydata.shape[0]):
#         plt.plot(x,mydata[i,:],alpha=0.6, lw=1.5)
#         plt.show()



import numpy as np
import matplotlib.pyplot as plt
import glob

filez = glob.glob("output\\*data.npy")
# meta = glob.glob("*meta.npy")

mydata = []
for file in filez:
    mydata.append(np.load(file))

maxes = []
sensor_with_max = 1
for data in mydata:
    # np.where(arr == np.amax(arr))
    maxes.append(np.where(data[sensor_with_max,:] == np.max(data[sensor_with_max,:]))[0][0])

shifted_data=[]
for i in range(len(maxes)):
    data = mydata[i][:,(maxes[i]-50):(maxes[i]+200)]
    shifted_data.append(data)

fig, axs = plt.subplots(mydata[0].shape[0], 1)
avgs = np.zeros(shifted_data[0].shape)

x=np.linspace(0,1/4370*shifted_data[0].shape[1],num=shifted_data[0].shape[1])
for trial in shifted_data:
    for i in range(shifted_data[0].shape[0]):
        axs[i].plot(x,trial[i,:],alpha=0.6,color="#BFBFBF", lw=1.5)
        avgs[i,:] += trial[i,:]


avgs = np.divide(avgs,len(filez))
for i in range(shifted_data[0].shape[0]):
    axs[i].plot(x,avgs[i,:], color="#0b53c1", lw=2.4, zorder=10)
    # axs[i].scatter(x, avgs[i,:], fc="w", ec="#0b53c1", s=60, lw=2.4, zorder=12) 



for i in range(len(axs)):
    axs[i].grid(True)


axs[0].set_title("Gastroc")
axs[1].set_title("TA")
axs[0].set_frame_on(False)
axs[1].set_frame_on(False)
plt.xlabel("Time (s)")
plt.show()
