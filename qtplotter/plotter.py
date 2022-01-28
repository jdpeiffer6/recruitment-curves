# Import libraries
import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
from collections import deque

### START QtApp #####
app = QtGui.QApplication([])            # you MUST do this once (initialize things)
###################r

win = pg.GraphicsLayoutWidget(show=True,title="Signal from serial port") # creates a window
p = win.addPlot(title="First plot",row=1,col=1)  # creates empty space for the plot in the window
p2 = win.addPlot(title="Second plot",row=2,col=1)
curve = p.plot()                        # create an empty "plot" (a curve to plot)
curve2 = p2.plot()

windowWidth = 10000                       # width of the window displaying the curve
Xm = np.linspace(0,0,windowWidth)          # create array that will contain the relevant time series     
ptr = -windowWidth                      # set first x position

# # Realtime data plot. Each time this function is called, the data display is updated
# def update():
#     global curve, ptr, Xm    
#     Xm[:-1] = Xm[1:]                      # shift data in the temporal mean 1 sample left
#     value = np.random.randn(1)                # read line (single value) from the serial port
#     Xm[-1] = float(value)                 # vector containing the instantaneous values      
#     ptr += 1                              # update x position for displaying the curve
#     curve.setData(Xm)                     # set the curve with this data
#     curve.setPos(ptr,0)                   # set x position in the graph to 0
#     QtGui.QApplication.processEvents()    # you MUST process the plot now

def update():
    global curve, d1,d2
    d1.append(float(np.random.randn(1)))
    d2.append(float(np.random.randn(1)))
    curve.setData(d1)                     # set the curve with this data
    curve2.setData(d2)
    # curve.setPos(ptr,0)                   # set x position in the graph to 0
    QtGui.QApplication.processEvents()    # you MUST process the plot now

### MAIN PROGRAM #####    
# this is a brutal infinite loop calling your realtime data plot
d1 = deque(np.zeros(10000),maxlen=10000)
d2=deque(np.zeros(10000),maxlen=10000)
while True:
    # d1[-1]=float(np.random.randn(1)
    update()

### END QtApp ####
pg.QtGui.QApplication.exec_() # you MUST put this at the end
##################