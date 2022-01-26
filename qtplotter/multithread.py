from PySide6.QtWidgets import QVBoxLayout, QLabel, QPushButton, QWidget, QMainWindow, QApplication
from PySide6.QtCore import QRunnable, Slot, QThreadPool

import sys
import time

# class Worker(QRunnable):
#     def __init__(self,*args,**kwargs):
#         super(Worker,self).__init__()
#         self.args=args
#         self.kwargs=kwargs
#     @Slot()
#     def run(self):
#         # your code here
#         print(self.args,self.kwargs)
#         print("Thread start")
#         time.sleep(5)
#         print("Thread complete")

class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    @Slot()  # QtCore.Slot
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        self.fn(*self.args, **self.kwargs)

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.counter = 0

        layout = QVBoxLayout()

        self.l = QLabel("Start")
        b = QPushButton("DANGER!")
        b.pressed.connect(self.oh_no)

        c = QPushButton("?")
        c.pressed.connect(self.change_message)

        layout.addWidget(self.l)
        layout.addWidget(b)

        layout.addWidget(c)

        w = QWidget()
        w.setLayout(layout)

        self.setCentralWidget(w)
        self.threadpool = QThreadPool()
        print("Multihreading with maximum of %d threads" % self.threadpool.maxThreadCount())
        self.show()

    def change_message(self):
        self.message = "OH NO"
    
    def execute_this_fn(self,invar):
        print(invar)

    def oh_no(self):
        worker = Worker(self.execute_this_fn,"Potato")
        self.threadpool.start(worker)

app = QApplication(sys.argv)
window = MainWindow()
app.exec_()