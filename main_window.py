from PyQt5.QtWidgets import (QMainWindow, QLabel, QDesktopWidget, QFrame)
from PyQt5.QtGui import (QPainter, QPen, QPixmap, QIcon, QColor)
from PyQt5.QtCore import Qt
import player

"""
centralni widget u MainWindow je mapa(matrica 16x16) = klasa Board
"""


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.width = 800
        self.height = 600
        self.map = Board(self)# mapa, za sad matrica 16x16
        self.label = QLabel(self)  # za sad nas player

        # instanciraj igraca
        self.player = player.Player(self.label, self.map)

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
        self.setWindowIcon(QIcon('images/PacManRightEat.png'))

        self.center_window()
        self.setCentralWidget(self.map)
        self.score_label.move(5, 5)
        self.score_label.setStyleSheet("font: 25pt Comic Sans MS; color: white")
        self.score_label.resize(150, 30)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))
        painter.drawRect(5, 40, self.width - 10, self.height - 50)

    def drawPlayer(self):
        self.pixmap = QPixmap("images/PacManRightEat.png")
        self.label.setPixmap(self.pixmap)
        self.label.move(240, 200)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.player.movePlayerLeft(self.label)
        elif event.key() == Qt.Key_Right:
            self.player.movePlayerRight(self.label)
        elif event.key() == Qt.Key_Up:
            self.player.movePlayerUp(self.label)
        elif event.key() == Qt.Key_Down:
            self.player.movePlayerDown(self.label)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.player.set_left_close(self.label)
        elif event.key() == Qt.Key_Right:
            self.player.set_right_close(self.label)
        elif event.key() == Qt.Key_Up:
            self.player.set_up_close(self.label)
        elif event.key() == Qt.Key_Down:
            self.player.set_down_close(self.label)


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

        # 0 => zid    1=> tunel  2=> Coin  3=> Eat_Ghost
        self.board = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0],
            [0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0],
            [0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0],
            [0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0],
            [0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 2, 1, 0],
            [0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1],
            [0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 0, 0, 1, 0, 1, 1, 1, 0],
            [0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0],
            [0, 2, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0],
            [0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 3, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

    def is_tunnel(self, x, y): # Vraca true ako je tunel, tj. omogucava kretanje PacMan-a. Ako je element matrice 0(zid) onda vraca false, tj. zabranjuje prolazak PacMan-a.
        if self.board[y//40][x//40] == 1:
            return True
        else:
            return False


    def paintEvent(self, event):
        painter = QPainter(self)

        for i in range(20):
            for j in range(16):
                if self.board[j][i] == 0:
                    #draw wall
                    self.draw_map(i*40, j*40, painter, Qt.darkBlue)
                elif self.board[j][i] == 2:
                    self.draw_coins(i, j, painter)
                elif self.board[j][i] == 3:
                    self.draw_eat_ghost_power(i, j, painter)
                else:
                    self.draw_map(i*40, j*40, painter, Qt.black) #tunel

    def draw_map(self, x, y, painter, color):
        painter.fillRect(x, y, 40, 40, color)

    def draw_coins(self, i, j, painter):
        painter.drawPixmap(i * 40, j *40, QPixmap('images/Coin.png'))

    def draw_eat_ghost_power(self, i, j, painter):
        painter.drawPixmap(i * 40, j *40, QPixmap('images/EatGhostsPower.png'))
