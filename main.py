import sys
from PyQt5.QtWidgets import QApplication
import start_menu


if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = start_menu.Menu()
    w.show()
    sys.exit(app.exec_())

