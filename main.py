from DataCollector.CollectDataController import *
from Display.Display import jdplot

plotter = jdplot()   # should rename this to logging
jdstreamer = PlottingManagement(plotter)

jdstreamer.Connect_Callback()
jdstreamer.Scan_Callback()

# mode = "EMG raw (4370 Hz), skin check (74 Hz), +/-11mv, 10-850Hz"
# jdstreamer.setSampleMode(0,mode)
# jdstreamer.setSampleMode(1,mode)
# a=jdstreamer.getCurMode()
# print(*a)
input("Ready?")
jdstreamer.Start_Callback()
print("Program done " + str(threading.get_native_id()))

# TODO: make my own class that can multithread collection and logging