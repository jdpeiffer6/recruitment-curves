# single-pulse-emg  

 ## AeroPy  
**DataManager** contains DataKernel class that seems to handle data streaming at the lowest level. In the future this could be a more efficient way to log.  
**TrignoBase** references the delsysAPI (although I dont think it works) and creates an instance of the TrignoBase.  
## daq  
**test** right now is just messing around with controlling the daq.  
## DataCollector  
**CollectDataController** controls data collection controller in class *PlottingManagment*. Has callbacks to handle multi threading, streaming, plotting, Connecting, Pairing, Scanning, Starting and Stopping the base. May want to combine this with the DataKernel class in the future.  
**CollectDataWindow** I don't think is used.  
## Display  
**Display** creates a space to log the data and logs it. Is incorperated into *PlottingManagement*.  