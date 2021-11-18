from collections import deque
import threading
import numpy as np
from time import sleep

class DataLogger():
    def __init__(self):
        self.data_queue = deque()
        self.setCollectionLen(15)
        self.pauseFlag = False
        self.threadManager()

    # region setup
    def setCollectionLen(self,n):
        self.data_log = np.zeros(n)
        self.dataLogIdx = 0

    # endregion

    # region data streaming and threading
    def getDataFromSensors(self):
        print("Getting Data From sensors " + str(threading.get_native_id()))
        dataReady = True
        while dataReady and not self.pauseFlag:
            self.data_queue.append( np.arange(5) )
        print("Finished getting data " + str(threading.get_native_id()))
    
    def logDataFromQueue(self):
        print("Starting log " + str(threading.get_native_id()))
        while not self.pauseFlag:
            if len(self.data_queue) >= 1:
                newData = self.data_queue.popleft()
                newDataLen = len(newData)
                self.data_log[self.dataLogIdx:(self.dataLogIdx+newDataLen)] = newData
                self.dataLogIdx += newDataLen
                if self.dataLogIdx > 14:
                    print("Completed Collection " + str(threading.get_native_id()))
                    self.pauseFlag = True
                    
    def threadManager(self):
        t1 = threading.Thread(target= self.getDataFromSensors)
        t2 = threading.Thread(target=self.logDataFromQueue)

        t1.start()
        t2.start()

    # endregion

    # region trigno control stuff



    # endregion
test_logger = DataLogger()
sleep(1)
print(test_logger.data_log)