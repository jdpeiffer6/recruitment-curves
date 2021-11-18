from collections import deque
import threading
import numpy as np
from AeroPy.TrignoBase import *

clr.AddReference("System.Collections")
from System.Collections.Generic import List
from System import Int32

from time import sleep



base = TrignoBase()
TrigBase = base.BaseInstance

class DataLogger():
    def __init__(self):
        self.data_queue = deque()

    # region setup
    def setCollectionLen(self, nChan, fs, l ):
        """Allocates empty data container for streaming based on number of seconds and channels"""
        # np arrays are row-major
        self.data_log = np.zeros([nChan, fs*(l+1)])
        self.dataLogIdx = 0
        self.dataLogMax = fs*l

    # endregion

    # region data streaming and threading
    def getDataFromSensors(self):
        """Gets data from trigno base"""
        print("Getting Data From sensors " + str(threading.get_native_id()))
        dataReady = True
        while dataReady and not self.pauseFlag:
            self.data_queue.append( np.arange(5) )
        print("Finished getting data " + str(threading.get_native_id()))
    
    def logDataFromQueue(self):
        """Gets data from self.data_queue and stores it in array. When collection is finished, stops collection."""
        print("Starting log " + str(threading.get_native_id()))
        while not self.pauseFlag:
            if len(self.data_queue) >= 1:
                newData = self.data_queue.popleft()
                newDataLen = len(newData)
                self.data_log[0, self.dataLogIdx:(self.dataLogIdx+newDataLen)] = newData
                self.dataLogIdx += newDataLen
                if self.dataLogIdx > self.dataLogMax:
                    print("Completed Collection " + str(threading.get_native_id()))
                    self.pauseFlag = True
                    self.Stop_Callback()
                    
    def threadManager(self):
        """Starts thread to run data retrevial and data logging."""
        t1 = threading.Thread(target= self.getDataFromSensors)
        t2 = threading.Thread(target=self.logDataFromQueue)

        t1.start()
        t2.start()

    # endregion

    # region trigno control stuff
    def Connect_Callback(self):
        """Callback to connect to the base"""
        TrigBase.ValidateBase(key, license, "RF")

    def Scan_Callback(self):
        """Callback to tell the base to scan for any available sensors"""
        f = TrigBase.ScanSensors().Result
        self.nameList = TrigBase.ListSensorNames()
        self.SensorsFound = len(self.nameList)

        TrigBase.ConnectSensors()
        return self.nameList


    def Start_Callback(self):
        """Callback to start the data stream from Sensors. Create output destination. And start threaded data collection."""

        self.pauseFlag = False
        newTransform = TrigBase.CreateTransform("raw")
        index = List[Int32]()

        TrigBase.ClearSensorList()

        for i in range(self.SensorsFound):
            selectedSensor = TrigBase.GetSensorObject(i)
            TrigBase.AddSensortoList(selectedSensor)
            index.Add(i)

        self.sampleRates = [[] for i in range(self.SensorsFound)]

        TrigBase.StreamData(index, newTransform, 2)

        self.dataStreamIdx = []
        plotCount = 0
        idxVal = 0
        for i in range(self.SensorsFound):
            selectedSensor = TrigBase.GetSensorObject(i)
            for channel in range(len(selectedSensor.TrignoChannels)):
                self.sampleRates[i].append((selectedSensor.TrignoChannels[channel].SampleRate,
                                           selectedSensor.TrignoChannels[channel].Name))
                print(selectedSensor.TrignoChannels[channel].Name)
                if "EMG" in selectedSensor.TrignoChannels[channel].Name:
                    self.dataStreamIdx.append(idxVal)
                    plotCount+=1
                idxVal += 1

        self.setCollectionLen(plotCount,int(self.sampleRates[0][0][0])+1,5)
        # TODO: figure out why this adds EMG and EMG B when switch to just raw EMG?
        self.threadManager()

    def Stop_Callback(self):
        """Callback to stop the data stream"""
        TrigBase.StopData()
        self.pauseFlag = True
        
    # endregion
