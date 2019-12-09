from PyQt5.QtWidgets import QWidget, QPushButton, QDesktopWidget, QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtCore import pyqtSlot
from main_window import MainWindow


class Menu(QWidget):
    def __init__(self):
        super().__init__()

        self.singlePlayer_btn = QPushButton('SinglePlayer', self)
        self.multiPlayer_btn = QPushButton('MultiPlayer', self)

        self.init_UI()

    def init_UI(self):
        self.setWindowTitle('Welcome to the game')
        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: black")

        self.singlePlayer_btn.setToolTip('Single player mode')
        self.singlePlayer_btn.move(200, 100)
        self.singlePlayer_btn.resize(400, 150)
        self.singlePlayer_btn.setStyleSheet("background-color: blue;"
                                            "font: 25pt Comic Sans MS;"
                                            "color: white;"
                                            "border-radius: 20px;")
        self.singlePlayer_btn.clicked.connect(self.on_click1)

        self.multiPlayer_btn.setToolTip('Multi player mode')
        self.multiPlayer_btn.move(200, 340)
        self.multiPlayer_btn.resize(400, 150)
        self.multiPlayer_btn.setStyleSheet("background-color: red;"
                                           "font: 25pt Comic Sans MS;"
                                           "color: white;"
                                           "border-radius: 20px;")
        self.multiPlayer_btn.clicked.connect(self.on_click2)


    @pyqtSlot()
    def on_click1(self):
        #kreiraj mainWindow sa jednim playerom
        self.mw = MainWindow()
        self.mw.show()
        self.close()

    @pyqtSlot()
    def on_click2(self):
        self.mw = MainWindow()
        self.mw.show()
        self.close()

    def center_window(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)
