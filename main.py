import sys
from PyQt5.QtWidgets import QApplication
import start_menu
import winsound


if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = start_menu.Menu()
    winsound.PlaySound("images/pacman_beginning.wav", winsound.SND_ASYNC | winsound.SND_ALIAS)
    w.show()
    sys.exit(app.exec_())

