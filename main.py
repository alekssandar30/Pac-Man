import sys
from PyQt5.QtWidgets import QApplication
import main_window


if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = main_window.MainWindow()
    sys.exit(app.exec_())

