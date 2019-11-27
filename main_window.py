#Ovde ce biti kod za lavirint

from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtGui import QPainter, QPen, QPixmap
from PyQt5.QtCore import Qt
import player


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.width = 700
        self.height = 650
        self.label = QLabel(self)

        self.score = 0
        self.score_label = QLabel('Score: ', self)

        self.init_ui()
        self.drawPlayer()

        self.show()

    def init_ui(self):

        self.setWindowTitle('Pac-Man')
        self.setFixedWidth(self.width)
        self.setFixedHeight(self.height)

        self.score_label.move(5, 15)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))
        painter.drawRect(5, 40, self.width-10, self.height-50)

    def drawPlayer(self):
        self.pixmap = QPixmap("images/pacman_o.png")
        self.label.setPixmap(self.pixmap)
        self.label.move(200, 200)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.movePlayerLeft(self.label)
        elif event.key()  == Qt.Key_Right:
            self.movePlayerRight(self.label)
        elif event.key() == Qt.Key_Up:
            self.movePlayerUp(self.label)
        elif event.key() == Qt.Key_Down:
            self.movePlayerDown(self.label)

    def movePlayerLeft(self, label):
        label.move(label.x()-5,label.y())

    def movePlayerRight(self, label):
        label.move(label.x()+5,label.y())

    def movePlayerUp(self, label):
        label.move(label.x(),label.y()-5)

    def movePlayerDown(self, label):
        label.move(label.x(),label.y()+5)

