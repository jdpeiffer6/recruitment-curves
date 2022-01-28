from deviceManager import *
from collections import deque
import threading
import numpy as np
from AeroPy.TrignoBase import *

clr.AddReference("System.Collections")
from System.Collections.Generic import List
from System import Int32

from time import sleep
from emg_acquisition_multithread import *
from daq.daq import mydaq
daq1 = mydaq()


deviceManager = deviceManager(TrigBase, daq1, 2300)