from PySide6 import QtGui  # (the example applies equally well to PySide2)
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout
import pyqtgraph as pg


app = QApplication([])

## Define a top-level widget to hold everything
w = QWidget()

## Create some widgets to be placed inside
btn = QPushButton('press me')
plot = pg.PlotWidget()

## Create a grid layout to manage the widgets size and position
layout = QGridLayout()
w.setLayout(layout)

## Add widgets to the layout in their proper positions
layout.addWidget(btn, 0, 0)   # button goes in upper-left
layout.addWidget(plot, 0, 1, 3, 1)  # plot goes on right side, spanning 3 rows

## Display the widget as a new window
w.show()

## Start the Qt event loop
app.exec_()