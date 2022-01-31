# Device Manager Script
# This script intializes the data collection system as its own object. 

import numpy as np
from AeroPy.TrignoBase import *

clr.AddReference("System.Collections")
from System.Collections.Generic import List
from System import Int32

base = TrignoBase()
TrigBase = base.BaseInstance

"Class takes a TrignoBase Object and an integer sampling rate (Hz), and 3 deques. deques are preliminry for the time being"
class deviceManager(): 
    def __init__(self,TrigBase, SamplingRate, deque1, deque2, deque3):
        self.TrigBase = TrigBase
        self.packetCount = 0
        self.sampleCount = 0 
        self.deque1 = deque1
        self.deque2 = deque2 
        self.deque3 = deque3

        self.SamplingRate = SamplingRate
        TrigBase.ClearSensorList()

        # Connect Callback
        TrigBase.ValidateBase(key, license, 'RF') #Connecting to Delsys Base Station        #Connect Callback
        print("\n Connected Base")

        #Scan Callback
        f = TrigBase.ScanSensors().Result                                                   #Scan Callback
        self.nameList = TrigBase.ListSensorNames() #returns sensor names that are paired
        self.SensorsFound = len(self.nameList) #counts number of sensors
        if self.SensorsFound == 0: 
            print('Error: No Sensors Successfully Paired')
            return 
        TrigBase.ConnectSensors()
        print("\n Scan Sensors")

        #Start callback
        self.Start_Callback()
        

    # region trigno control stuff

    def Start_Callback(self):
        """Callback to start the data stream from Sensors. Create output destination."""
        print('Starting Callback')
        self.pauseFlag = False
        newTransform = TrigBase.CreateTransform("raw")
        index = List[Int32]()

        # TrigBase.ClearSensorList()

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

        #start collecting data now
        # self.threadManager()
        print("Started Streaming")

    # TODO: Need to incorporate multi-sensor functionality to process and get data functions, as right now they work but only on
    #  one paired sensor. Streaming and plotting in real time is functional however. 

    def processData(self):
        "Processes Trignobase Data from Delsys and place into deque passed into function"
        outArray = self.GetData()
        param = (len(self.dataStreamIdx),52)
        # TODO: 52 may not be constant packet size, need to automate!
        filler = np.zeros(param)
        if outArray is not None:
            # for k in range(TrigBase.SensorsFound): #indexing via sensor
                for i in self.dataStreamIdx:
                    # Appends EMG Data (52 packets per sample)
                    for j in range(outArray[0][0].shape[0]):
                        # self.deque1.append(outArray[0][0][j])
                        # self.deque2.append(outArray[4][0][j])
                        # self.deque3.append(outArray[8][0][j])

                        filler[int(i/4)][j] = (outArray[i][0][j])

                    # Appends Gyro Data (4 packets per sample)
                    for j in range(outArray[1][0].shape[0]):
                        pass 
                    try: 
                        self.packetCount += len(outArray[0])
                        self.sampleCount += len(outArray[0][0])
                    except: 
                        pass
                self.deque1.append(filler)
                print("data filled")
                    # TODO: actually put data in correct data_queues
                    # TODO: probaly dont need the try/exception here
                


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

    # def streaming(self):
    #     while self.pauseFlag is False:
    #         self.
           
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