from PyQt5.QtCore import QRunnable, pyqtSlot

class Worker(QRunnable):
    def __init__(self, fun, *args, **kwargs):
        super(Worker, self).__init__()
        self.fun = fun
        self.args = args
        self.kwargs = kwargs

    @pyqtSlot()
    def run(self):
        self.fun()