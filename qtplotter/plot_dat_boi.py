import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout,QPushButton
from PySide6.QtCore import QTimer,QRunnable,Slot,QThreadPool
import pyqtgraph as pg
import numpy as np
from collections import deque
import random
import time

class Worker(QRunnable):
    def __init__(self,*args,**kwargs):
        super(Worker,self).__init__()
        self.args=args
        self.kwargs=kwargs
    @Slot()
    def run(self):
        print("Starting Worker thread")
        # your code here
        t=0
        while not self.args[-1][0]:
            time.sleep(0.01)
            t+=1
            self.args[0].append(random.random())
            self.args[1].append(t//10)
            self.args[2].append(np.sin(0.2*t))
 

class myWidget(QWidget):
    def __init__(self,in_queue,in_queue2,in_queue3,device):
        super(myWidget, self).__init__()

        # QTstuff
        self.button = QPushButton("Start")
        self.button.pressed.connect(self.start_callback)
        self.button2 = QPushButton("Stop")
        self.button2.pressed.connect(self.stop_callback)

        layout = QVBoxLayout()
        self.plot = pg.GraphicsLayoutWidget(title="Signal")
        layout.addWidget(self.plot)
        layout.addWidget(self.button)
        layout.addWidget(self.button2)
        self.setLayout(layout)
        self.p = self.plot.addPlot(row=1, col=1)
        self.p2 = self.plot.addPlot(row=2, col=1)
        self.p3 = self.plot.addPlot(row=3, col=1)
        self.curve = self.p.plot()  # create an empty "plot" (a curve to plot)
        self.curve2 = self.p2.plot()
        self.curve3 = self.p3.plot()

        self.timer = QTimer()
        self.timer.setInterval(30)
        self.timer.timeout.connect(self.update)
        self.timer.start()

        # queue stuff
        self.queue = in_queue
        self.queue2 = in_queue2
        self.queue3 = in_queue3

        #thread stuff
        self.threadpool = QThreadPool()
        print("Multihreading with maximum of %d threads" % self.threadpool.maxThreadCount())

    def update(self):
        # self.queue.append(random.random())
        self.curve.setData(np.array(self.queue))
        self.curve2.setData(np.array(self.queue2))
        self.curve3.setData(np.array(self.queue3))
        super(myWidget, self).update()

    def start_callback(self):
        print("Started Worker")
        self.stop_flag = [False]
        worker = Worker(self.queue, self.queue2, self.queue3, self.stop_flag)
        self.threadpool.start(worker)

    def stop_callback(self):
        print("Stopp flag set")
        self.stop_flag[0] = True

if __name__ == "__main__":

    app = QApplication(sys.argv)
    my_queue = deque(maxlen=500)
    my_queue2 = deque(maxlen=500)
    my_queue3 = deque(maxlen=500)
    device = 5
    widget = myWidget(my_queue,my_queue2,my_queue3,device)
    widget.show()
    app.exec()