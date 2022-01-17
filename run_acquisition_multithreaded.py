from emg_acquisition_multithread import *
from daq.daq import mydaq
daq1 = mydaq()

test_logger = DataLogger(TrigBase,daq1)

test_logger.Connect_Callback()
test_logger.Scan_Callback()
test_logger.setSampleMode("EMG raw (4370 Hz), skin check (74 Hz), +/-11mv, 10-850Hz")
# test_logger.Start_Callback(0.1)

n_trials = 3
for _ in range(n_trials):
    test_logger.Start_Callback(0.3)
    test_logger.trig()
    test_logger.Stop_Callback()

test_logger.Stop_Callback()
import output.analyze
print("Done")