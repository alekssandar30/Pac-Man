from PyQt5.QtWidgets import (QMainWindow, QLabel, QDesktopWidget, QFrame)
from PyQt5.QtGui import (QPainter, QPen, QPixmap, QIcon, QColor)
from PyQt5.QtCore import Qt

"""
centralni widget u MainWindow je mapa(matrica 16x16) = klasa Board
"""


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.width = 800
        self.height = 600
        self.label = QLabel(self)  # za sad nas player
        self.map = Board(self)  # mapa, za sad matrica 16x16

        self.score = 0
        self.score_label = QLabel('Score: ', self)

        self.init_ui()
        self.drawPlayer()

        self.enemies = []  # u ove liste cemo dodavati protivnike i hranu
        self.food = []

        self.show()

    def init_ui(self):

        self.setWindowTitle('Pac-Man')
        self.setFixedWidth(self.width)
        self.setFixedHeight(self.height)
        self.setWindowIcon(QIcon('images/player.png'))

        self.center_window()
        self.setCentralWidget(self.map)
        self.score_label.move(5, 15)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))
        painter.drawRect(5, 40, self.width - 10, self.height - 50)

    def drawPlayer(self):
        self.pixmap = QPixmap("images/pacman_o.png")
        self.label.setPixmap(self.pixmap)
        self.label.move(200, 200)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.movePlayerLeft(self.label)
        elif event.key() == Qt.Key_Right:
            self.movePlayerRight(self.label)
        elif event.key() == Qt.Key_Up:
            self.movePlayerUp(self.label)
        elif event.key() == Qt.Key_Down:
            self.movePlayerDown(self.label)

    def movePlayerLeft(self, label):
        label.move(label.x() - 5, label.y())

    def movePlayerRight(self, label):
        label.move(label.x() + 5, label.y())

    def movePlayerUp(self, label):
        label.move(label.x(), label.y() - 5)

    def movePlayerDown(self, label):
        label.move(label.x(), label.y() + 5)

    """Center screen"""

    def center_window(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)


class Board(QFrame):
    board_width = 800
    board_height = 600

    def __init__(self, parent):
        super().__init__(parent)

        self.resize(self.board_width, self.board_height)

        # 0 => zid    1=> tunel
        self.board = [
             1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0,
             1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0,
             1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
             1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0,
             1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0,
             0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
             0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0,
             0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0,
             0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0,
             0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0,
             1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0,
             1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0,
             1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0,
             0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0,
             1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0,
             1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0,

        ]


    """
    def paintEvent(self, event):
        painter = QPainter(self)
        #ovde treba ispraviti
        for i in range(16):
            for j in range(16):
                if self.board[i][j] == 0:
                    #draw wall
                    self.draw_map(i, j, painter, Qt.darkBlue)
                else:
                    self.draw_map(i, j, painter, Qt.black) #tunel

    def draw_map(self, x, y, painter, color):
        pass
    """
