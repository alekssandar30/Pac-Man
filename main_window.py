from PyQt5.QtWidgets import (QMainWindow, QLabel, QDesktopWidget, QFrame)
from PyQt5.QtGui import (QPainter, QPen, QPixmap, QIcon, QColor, QMovie)
from PyQt5.QtCore import Qt
import player
import enemy

"""
centralni widget u MainWindow je mapa(matrica 16x16) = klasa Board
"""


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.width = 800
        self.height = 640
        self.map = Board(self)

        # Labele
        self.label = QLabel(self)  # za sad nas player
        self.blue_ghost = QLabel(self)
        self.orange_ghost = QLabel(self)
        self.red_ghost = QLabel(self)
        self.yellow_ghost = QLabel(self)

        self.title_label = QLabel('PacMan',self)
        self.label_for_player_score = QLabel(self)
        self.score_label = QLabel('Score: ', self)
        self.label_for_coin_display = QLabel(self)

        # instanciraj igraca i protivnike
        self.player = player.Player(self.label, self.map, self.label_for_player_score)
        self.ghost1 = enemy.Enemy(self.blue_ghost, self.map, self.player)
        self.ghost2 = enemy.Enemy(self.orange_ghost, self.map, self.player)
        self.ghost3 = enemy.Enemy(self.red_ghost, self.map, self.player)
        self.ghost4 = enemy.Enemy(self.yellow_ghost, self.map, self.player)

        ## Special power
        self.label_super_power = QLabel(self)
        self.movie = QMovie('images/SpecialPowers.gif')
        self.label_super_power.move(self.map.special_power_locations[0], self.map.special_power_locations[1])
        self.label_super_power.resize(40, 40)
        self.label_super_power.setMovie(self.movie)
        self.movie.start()
        ##

        self.init_ui()
        self.drawPlayer()
        self.draw_ghosts()
        self.initPlayerScore()

        self.enemies = []
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
        self.score_label.setStyleSheet("font: 20pt Comic Sans MS; color: white")
        self.score_label.resize(150, 30)

        self.title_label.setStyleSheet("font: 22pt Comic Sans MS; color: white")
        self.title_label.move(350,5)
        self.title_label.resize(150, 30)

        self.label_for_coin_display.setPixmap(QPixmap("images/ResultCoins.png"))
        self.label_for_coin_display.move(110, 5)
        self.label_for_coin_display.resize(30,30)

    def drawPlayer(self):
        self.pixmap = QPixmap("images/PacManRightEat.png")
        self.label.setPixmap(self.pixmap)
        self.label.resize(40,40)
        self.label.setStyleSheet("background:transparent")
        self.label.move(720, 560)

    #iscrtavanje protivnika
    def draw_ghosts(self):
        self.blue_ghost_pixmap = QPixmap("images/GhostBlueDown1.png")
        self.orange_ghost_pixmap = QPixmap("images/GhostOrangeDown1.png")
        self.red_ghost_pixmap = QPixmap("images/GhostRedDown1.png")
        self.yellow_ghost_pixmap = QPixmap("images/GhostYellowDown1.png")

        self.blue_ghost.setPixmap(self.blue_ghost_pixmap)
        self.orange_ghost.setPixmap(self.orange_ghost_pixmap)
        self.red_ghost.setPixmap(self.red_ghost_pixmap)
        self.yellow_ghost.setPixmap(self.yellow_ghost_pixmap)

        self.blue_ghost.resize(40, 40)
        self.orange_ghost.resize(40, 40)
        self.red_ghost.resize(40, 40)
        self.yellow_ghost.resize(40, 40)

        self.blue_ghost.move(370, 370)
        self.red_ghost.move(400, 400)
        self.orange_ghost.move(400, 330)
        self.yellow_ghost.move(520, 320)

    def initPlayerScore(self):
        self.label_for_player_score.setText('0')
        self.label_for_player_score.setStyleSheet("font: 20pt Comic Sans MS; color: white")
        self.label_for_player_score.move(135,5)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.player.movePlayerLeft(self.label)
        elif event.key() == Qt.Key_Right:
            self.player.movePlayerRight(self.label)
        elif event.key() == Qt.Key_Up:
            self.player.movePlayerUp(self.label)
        elif event.key() == Qt.Key_Down:
            self.player.movePlayerDown(self.label)

    """Center screen"""

    def center_window(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)



class Board(QFrame):
    board_width = 800
    board_height = 640

    def __init__(self, parent):
        super().__init__(parent)

        self.resize(self.board_width, self.board_height)
        # 0 => zid    1=> tunel  2=> Coin  3=> Eat_Ghost 4=> SpecialPowers
        self.board = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 3, 2, 2, 0, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 0, 2, 2, 4, 0],
            [0, 2, 0, 2, 2, 2, 0, 0, 0, 2, 2, 2, 0, 0, 2, 2, 2, 0, 2, 0],
            [0, 2, 2, 2, 0, 2, 2, 2, 2, 2, 0, 2, 2, 0, 2, 0, 3, 2, 2, 0],
            [0, 0, 2, 0, 0, 2, 2, 0, 2, 3, 0, 2, 2, 2, 2, 2, 0, 2, 2, 0],
            [0, 2, 2, 2, 0, 0, 2, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 0, 2, 0],
            [0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 0, 2, 0, 0, 2, 0, 0, 2, 2, 0],
            [0, 2, 2, 3, 2, 2, 0, 2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0],
            [2, 2, 2, 0, 0, 2, 2, 2, 0, 0, 1, 0, 0, 2, 0, 0, 0, 2, 2, 2],
            [0, 0, 2, 0, 0, 2, 0, 2, 0, 1, 1, 1, 0, 2, 2, 0, 3, 0, 2, 0],
            [0, 2, 2, 2, 2, 2, 2, 2, 0, 1, 1, 1, 0, 0, 2, 0, 2, 2, 2, 0],
            [0, 2, 0, 2, 0, 0, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 2, 0],
            [0, 2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 0, 2, 0],
            [0, 3, 2, 2, 0, 2, 0, 0, 0, 3, 0, 2, 2, 0, 2, 2, 2, 2, 2, 0],
            [0, 2, 0, 2, 2, 2, 0, 0, 0, 2, 2, 2, 0, 0, 2, 2, 2, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],]

        self.special_power_locations = []
        self.populate_super_power_indices(self.board, 4) # vraca indekse svih elemenata cija je vrednost 4 iz matrice board


    def is_tunnel(self, x, y): # Vraca true ako je tunel, tj. omogucava kretanje PacMan-a. Ako je element matrice 0(zid) onda vraca false, tj. zabranjuje prolazak PacMan-a.
        if (x % 40 == 0 and y % 40 == 0):
            if self.board[y//40][x//40] == 1:
                return True
        else:
            return False

    def is_coin(self, x, y):
        if (x % 40 == 0 and y % 40 == 0):
            if self.board[y // 40][x // 40] == 2:
                return True
        else:
            return False

    def is_eat_ghosts_power(self, x, y):
        if (x % 40 == 0 and y % 40 == 0):
            if self.board[y // 40][x // 40] == 3:
                return True
        else:
            return False

    def zid(self, x, y):
        if (x % 40 == 0 and y % 40 == 0):
            if x == 800:
                return True
            if x == -40:
                return True
            if self.board[y // 40][x // 40] != 0:
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
                elif self.board[j][i] == 4:
                    self.draw_map(i * 40, j * 40, painter, Qt.black) # Za pocetak da crta tunel
                else:
                    self.draw_map(i*40, j*40, painter, Qt.black) #tunel

    def draw_map(self, x, y, painter, color):
        painter.fillRect(x, y, 40, 40, color)

    def draw_coins(self, i, j, painter):
        painter.drawPixmap(i * 40, j *40, QPixmap('images/Coin.png'))

    def draw_black_background(self, x, y):  # Kad PacMan "pojede" coin, coin se zamenjuje crnom slikom
        self.board[y // 40][x // 40] = 1

    def draw_eat_ghost_power(self, i, j, painter):
        painter.drawPixmap(i * 40, j * 40, QPixmap('images/EatGhostsPower1.png'))

    def populate_super_power_indices(self, board, value):
        for i in range(20):
            for j in range(16):
                if board[j][i] == value:
                    self.special_power_locations.append(i * 40)
                    self.special_power_locations.append(j * 40)