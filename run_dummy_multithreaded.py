from dummy_multithread import *


test_logger = DataLogger()

test_logger.Connect_Callback()
test_logger.Scan_Callback()
test_logger.Start_Callback()

sleep(1)
print("Done")