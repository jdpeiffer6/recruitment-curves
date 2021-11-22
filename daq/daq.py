import nidaqmx
import numpy as np
from nidaqmx import stream_writers

class mydaq:
    def __init__(self):
        self.task = nidaqmx.Task()
        self.task.ao_channels.add_ao_voltage_chan('Dev1/ao0')
        self.task.timing.cfg_samp_clk_timing(5000,samps_per_chan=2) 

        self.stream = stream_writers.AnalogSingleChannelWriter(self.task.out_stream,auto_start=True)
        self.array = np.zeros(2,dtype=np.float64)
        self.array[0] = 5

    def __del__(self):
        self.task.close()

    def trig(self):
        self.stream.write_many_sample(self.array)
        self.task.wait_until_done()
        self.task.stop()