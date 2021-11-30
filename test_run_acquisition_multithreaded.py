from emg_acquisition_multithread import *
from daq.daq import mydaq
daq1 = mydaq()

test_logger = DataLogger(TrigBase,daq1)

test_logger.Connect_Callback()
test_logger.Scan_Callback()
test_logger.setSampleMode("EMG raw (4370 Hz), skin check (74 Hz), +/-11mv, 10-850Hz")
test_logger.test_setup(0.3)

n_trials = 15
for _ in range(n_trials):
    test_logger.test_run()

test_logger.Stop_Callback()
import output.analyze
print("Done")