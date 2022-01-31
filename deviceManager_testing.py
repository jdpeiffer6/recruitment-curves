from trialDeviceManager import *
from collections import deque






dummy1 = deque()
dummy2 = deque()
dummy3 = deque()
deviceManager = deviceManager(TrigBase, 2300, dummy1, dummy2, dummy3)
for i in range(1000000):
    deviceManager.processData()

print(deviceManager.deque1)