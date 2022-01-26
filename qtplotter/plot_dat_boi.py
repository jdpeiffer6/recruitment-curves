import queue
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PySide6.QtGui import QPalette, QColor
import pyqtgraph as pg
import numpy as np
from collections import deque

class MainWindow(QMainWindow):

    def __init__(self,q1,q2):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")

        layout = QVBoxLayout()

        plot = pg.GraphicsLayoutWidget(show=True,title="Signal from serial port") # creates a window
        layout.addWidget(plot)

        p = plot.addPlot(title="First plot",row=1,col=1)  # creates empty space for the plot in the window
        p2 = plot.addPlot(title="Second plot",row=2,col=1)
        self.curve = p.plot()                        # create an empty "plot" (a curve to plot)
        self.curve2 = p2.plot()

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.queue1 = q1
        q1.append(np.random.randn(5000))
        self.queue2 = q2

    def update(self):
        self.curve.setData(np.random.randn(500))                     # set the curve with this data
        self.curve2.setData(self.queue2)
        QApplication.processEvents()
        # QtGui.QApplication.processEvents()    # you MUST process the plot now

app = QApplication(sys.argv)
de1=deque(maxlen=5000)
de2=deque(maxlen=5000)
de1.append(np.random.randn(5000))
window = MainWindow(de1,de2)
window.show()
de1.append(np.random.randn(5000))
de2.append(np.random.randn(5000))
app.exec_()