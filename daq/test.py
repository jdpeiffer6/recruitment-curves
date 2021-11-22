# from enum import auto
# import nidaqmx
# import numpy as np

# region stupid
# t = np.linspace(start = 0, stop = 100, num = 10000)
# A = 5
# y = A*np.sin(t)
# with nidaqmx.Task() as task:
#     task.ao_channels.add_ao_voltage_chan("Dev1/ao0")
#     task.write(y,auto_start=True)
#     task.write(0,auto_start=True)
#     task.stop()


# # ao sw timed
# test = np.zeros(2,dtype = int)
# test[0] = 5
# with nidaqmx.Task() as task:
#     task.ao_channels.add_ao_voltage_chan('Dev1/ao0')
#     task.timing.
#     print('1 Channel 2 Sample Write: ')
#     print(task.write(test,auto_start=True))
#     task.stop()

#     # print('1 Channel N Samples Write: ')
#     # print(task.write([1.1, 2.2, 3.3, 4.4, 5.5], auto_start=True))
#     # task.write(0,auto_start=True)
#     # task.stop()

#     # task.ao_channels.add_ao_voltage_chan('Dev1/ao1')

#     # print('N Channel 1 Sample Write: ')
#     # print(task.write([1.1, 2.2]))
#     # task.stop()

#     # print('N Channel N Samples Write: ')
#     # print(task.write([[1.1, 2.2, 3.3], [1.1, 2.2, 4.4]],
#     #                  auto_start=True))
#     # task.stop()


# # ao hw timed works
# import numpy as np
# test = 2*np.ones([1000])
# test[-1] = 0
# with nidaqmx.Task() as task:
#     task.ao_channels.add_ao_voltage_chan('Dev1/ao0')

#     task.timing.cfg_samp_clk_timing(1000)

#     print('1 Channel N Samples Write: ')
#     print(task.write(test, auto_start=True))
#     task.wait_until_done()
#     task.stop()


# hw timed works
# import numpy as np
# test = np.zeros(100,dtype=int)
# test[0] = 5
# with nidaqmx.Task() as task:
#     task.ao_channels.add_ao_voltage_chan('Dev1/ao0')

#     task.timing.cfg_samp_clk_timing(5000)
#     task.write(test, auto_start=True)
#     task.wait_until_done()
#     task.stop()


# # stream writer with software timer
# from nidaqmx import stream_writers
# task = nidaqmx.Task()
# task.ao_channels.add_ao_voltage_chan('Dev1/ao0')
# stream = stream_writers.AnalogSingleChannelWriter(task.out_stream,auto_start=True)
# stream.write_many_sample(np.array([5,0],dtype=np.float64))
# task.stop()
# task.close()
# endregion

#stream writer with hardware timer. this is how i think i will do it
import nidaqmx
import numpy as np
from nidaqmx import stream_writers
task = nidaqmx.Task()
task.ao_channels.add_ao_voltage_chan('Dev1/ao0')
task.timing.cfg_samp_clk_timing(5000,samps_per_chan=2)   
#the samps per channel argument is pretty important because if:
#  (number of input samples to write) < (samps per channel), then the daq will just loop.

stream = stream_writers.AnalogSingleChannelWriter(task.out_stream,auto_start=True)
array = np.zeros(2,dtype=np.float64)
array[0] = 5


stream.write_many_sample(array)
task.wait_until_done()
task.stop()
task.close()

# i do not think our device does harware triggering
# import nidaqmx
# from nidaqmx import constants
# import numpy as np

# def event_callback(task_handle, signal_type, callback_data):
#     print("Called")

# with nidaqmx.Task() as task:
#     task.ao_channels.add_ao_voltage_chan('Dev1/ao0')
#     task.timing.cfg_samp_clk_timing(1)
#     task.triggers.start_trigger.cfg_dig_edge_start_trig('Dev1/port2/line0:0')
#     # task.register_signal_event(constants.TriggerType.DIGITAL_EDGE,event_callback)
#     task.start()


# sw timed reading
# import nidaqmx

# from nidaqmx.constants import (LineGrouping)

# with nidaqmx.Task() as task:
#     task.di_channels.add_di_chan('Dev1/port2/line0',line_grouping=LineGrouping.CHAN_PER_LINE)

#     print('1 Channel N Samples Read: ')
#     data = task.read(number_of_samples_per_channel=100)
#     while not any(data):
#         data = task.read(number_of_samples_per_channel=100)
#         task.stop()
#     print("Triggered")
