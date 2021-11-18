from dummy_multithread import *


test_logger = DataLogger(TrigBase)

test_logger.Connect_Callback()
test_logger.Scan_Callback()
test_logger.setSampleMode("EMG raw (4370 Hz), skin check (74 Hz), +/-11mv, 10-850Hz")
test_logger.Start_Callback(5)

print("Done")