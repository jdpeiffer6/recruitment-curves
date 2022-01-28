# Device Manager Script
# This script intializes the data collection system as its own object. 

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

"Class takes a TrignoBase Object and an integer sampling rate (Hz), and 3 deques. deques are preliminry for the time being"
class deviceManager(): 
    def __init__(self,TrigBase, daq, SamplingRate, deque1, deque2, deque3):
        self.TrigBase = TrigBase
        self.daq = daq
        self.packetCount = 0
        self.sampleCOunt = 0 
        self.stimcount = 0
        # self.data_queue = deque()
        # self.stim_queue = deque()
        self.deque1 = deque1
        self.deque2 = deque2 
        self.deque3 = deque3
        self.SamplingRate = SamplingRate
        TrigBase.ValidateBase(key, license, 'RF') #Connecting to Delsys Base Station        #Connect Callback
        f = TrigBase.ScanSensors().Result                                                   #Scan Callback
        self.nameList = TrigBase.ListSensorNames() #returns sensor names that are paired
        self.SensorsFound = len(self.nameList) #counts number of sensors
        if self.SensorsFound == 0: 
            print('Error: No Sensors Successfully Paired')
            return 

        TrigBase.ConnectSensors()

    # region trigno control stuff

    def Start_Callback(self,collection_time):
        """Callback to start the data stream from Sensors. Create output destination."""

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


        sleep(2)  # TODO: figure out why there is a random rise in this data
        # self.threadManager()

    def processData(self, data_queue):
        "Processes Trignobase Data from Delsys and place into deque passed into function"
        outArray = self.GetData()
        if outArray is not None:
            for i in range(len(outArray[0])):
                data_queue.append(list(np.asarray(outArray)[:,i]))
                # TODO 
            try: 
                self.packetCount += len(outArray[0])
                self.sampleCount += len(outArray[0][0])
            except: 
                pass
        


    def GetData(self):
        """Callback to get the data from the streaming sensors"""
        dataReady = self.TrigBase.CheckDataQueue()
        if dataReady:
            DataOut = self.TrigBase.PollData()
            if len(DataOut) > 0:  # Check for lost Packets
                outArr = [[] for i in range(len(DataOut))]
                for j in range(len(DataOut)):
                    for k in range(len(DataOut[j])):
                        outBuf = DataOut[j][k]
                        outArr[j].append(np.asarray(outBuf))
                return outArr
            else:
                return None
        else:
            return None

    # region Helpers
    def getPacketCount(self):
        return self.packetCount

    def resetPacketCount(self):
        self.packetCount = 0
        self.sampleCount = 0

    def getSampleCount(self):
        return self.sampleCount

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
            "EMG raw (4370 Hz), skin check (74 Hz), +/-11mv, 10-850Hz"
    # endregion
