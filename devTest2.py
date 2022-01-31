from trialDeviceManager import *
from collections import deque
from qtplotter.myWidget import *

if __name__ == "__main__":

    app = QApplication([])
    maxlen = 10000
    my_queue = deque(maxlen=maxlen)
    my_queue2 = deque(maxlen=int(maxlen))
    my_queue3 = deque(maxlen=int(maxlen))

    deviceManager = deviceManager(TrigBase, 2300, my_queue, my_queue2, my_queue3)

    widget = myWidget(my_queue,my_queue2,my_queue3,deviceManager)
    widget.show()
    app.exec_()