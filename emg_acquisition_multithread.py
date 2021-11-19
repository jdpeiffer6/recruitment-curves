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
    def __init__(self, trigbase):
        self.TrigBase = trigbase
        self.packetCount = 0
        self.sampleCount = 0

        self.data_queue = deque()

    # region setup
    def setCollectionLen(self, nChan, fs, collection_time ):
        """Allocates empty data container for streaming based on number of seconds and channels"""
        # np arrays are row-major
        self.data_log = np.zeros([nChan, fs*(collection_time+1)])
        self.dataLogIdx = 0
        self.dataLogMax = fs*collection_time

    # endregion

    # region data streaming and threading
    def getDataFromSensors(self):
        """Gets data from trigno base"""
        print("\n\n\n\n\nGetting Data From sensors " + str(threading.get_native_id()))
        while not self.pauseFlag:
            #if there is data to get
            if self.TrigBase.CheckDataQueue():
                DataOut = self.TrigBase.PollData()
                if len(DataOut) > 0:  # Check for lost Packets
                    outArr = [[] for i in range(len(self.dataStreamIdx))]
                    for j in range(len(self.dataStreamIdx)):
                        # right now getting data from 0, 2, ... channels (found in self.dataStreamIdx)
                        outArr[j].append(np.asarray(DataOut[self.dataStreamIdx[j]][0]))
                        # TODO: this may not actuall be the case so watch out
                    self.data_queue.append(outArr)
        print("Finished getting data " + str(threading.get_native_id()))
    
    # SOMEWHAT MESSED WITH
    # def getDataFromSensors(self):
    #     """Gets data from trigno base"""
    #     print("\n\n\n\n\nGetting Data From sensors " + str(threading.get_native_id()))
    #     while not self.pauseFlag:
    #         #if there is data to get
    #         if self.TrigBase.CheckDataQueue():
    #             DataOut = self.TrigBase.PollData()
    #             if len(DataOut) > 0:  # Check for lost Packets
    #                 outArr = [[] for i in range(len(DataOut))]
    #                 for j in range(len(DataOut)):
    #                     for k in range(len(DataOut[j])):
    #                         outBuf = DataOut[j][k]
    #                         outArr[j].append(np.asarray(outBuf))
    #                 self.data_queue.append([outArr[jd] for jd in self.dataStreamIdx])
    #                 # TODO: this could be optimized because right now we are grabbing the accelrometer data/EMG B too. If we never collect it, it may not be a problem.
    #                 #could also use slicing: list[0:5:4]
    #     print("Finished getting data " + str(threading.get_native_id()))

    #NOT MESSED WITH
    # def getDataFromSensors(self):
    #     """Gets data from trigno base"""
    #     print("Getting Data From sensors " + str(threading.get_native_id()))
    #     while not self.pauseFlag:
    #         #if there is data to get
    #         if self.TrigBase.CheckDataQueue():
    #             DataOut = self.TrigBase.PollData()
    #             if len(DataOut) > 0:  # Check for lost Packets
    #                 outArr = [[] for i in range(len(DataOut))]
    #                 for j in range(len(DataOut)):
    #                     for k in range(len(DataOut[j])):
    #                         outBuf = DataOut[j][k]
    #                         outArr[j].append(np.asarray(outBuf))
    #                 self.data_queue.append(outArr)
    #     print("Finished getting data " + str(threading.get_native_id()))

    def logDataFromQueue(self):
        """Gets data from self.data_queue and stores it in array. When collection is finished, stops collection."""
        print("Starting log " + str(threading.get_native_id()))
        while not self.pauseFlag:
            if len(self.data_queue) >= 1:
                newData = self.data_queue.popleft()
                newDataLen = len(newData[0][0])
                if len(newData) != self.data_log.shape[0]:
                    print("ERROR: Number of data streams does not match. logDataFromQueue")
                for i in range(len(newData)):
                    self.data_log[i, self.dataLogIdx:(self.dataLogIdx+newDataLen)] = newData[i][0]
                self.dataLogIdx += newDataLen
                if self.dataLogIdx > self.dataLogMax:
                    print("Completed Collection " + str(threading.get_native_id()))
                    self.pauseFlag = True
                    self.Stop_Callback()
                    np.save("output\\dummy_multithread.npy",self.data_log[:,0:self.dataLogIdx])
                    
    def threadManager(self):
        """Starts thread to run data retrevial and data logging."""
        t1 = threading.Thread(target= self.getDataFromSensors)
        t2 = threading.Thread(target=self.logDataFromQueue)

        t1.start()
        t2.start()

        t1.join()
        t2.join()

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

    def Start_Callback(self,collection_time):
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

        # TODO: maybe figure out if I can trigger collection with this?
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
                #changed in to == here
                # if "EMG" in selectedSensor.TrignoChannels[channel].Name:
                if "EMG" == selectedSensor.TrignoChannels[channel].Name:
                    self.dataStreamIdx.append(idxVal)
                    plotCount+=1
                idxVal += 1

        self.setCollectionLen(plotCount,int(self.sampleRates[0][0][0])+1,collection_time)
        # TODO: figure out why this adds EMG and EMG B when switch to just raw EMG?


        # sleep(2)  # TODO: figure out why there is a random rise in this data
        self.threadManager()

    def Stop_Callback(self):
        """Callback to stop the data stream"""
        TrigBase.StopData()
        self.pauseFlag = True
        
    # endregion

    # region Helper functions
    def getSampleModes(self,sensorIdx):
        """Gets the list of sample modes available for selected sensor"""
        sampleModes = TrigBase.ListSensorModes(sensorIdx)
        return sampleModes

    def getCurMode(self):
        """Gets the current mode of the sensors"""
        curMode = TrigBase.GetSampleMode()
        return curMode

    def setSampleMode(self,setMode):
        """Sets the sample mode for the selected sensor"""
        for i in range(len(self.getCurMode())):
            TrigBase.SetSampleMode(i,setMode)
    # endregion
