from enum import auto
import nidaqmx
import numpy as np

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


#stream writer with hardware timer. this is how i think i will do it
from nidaqmx import stream_writers
task = nidaqmx.Task()
task.ao_channels.add_ao_voltage_chan('Dev1/ao0')
task.timing.cfg_samp_clk_timing(5000,samps_per_chan=2)

stream = stream_writers.AnalogSingleChannelWriter(task.out_stream,auto_start=True)
array = np.zeros(2,dtype=np.float64)
array[0] = 5

stream.write_many_sample(array)
task.wait_until_done()
task.stop()
task.close()