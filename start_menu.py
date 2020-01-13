from PyQt5.QtWidgets import QWidget, QPushButton, QDesktopWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QLineEdit, QLabel
from PyQt5.QtCore import pyqtSlot, QSize
from main_window import MainWindow
from PyQt5.QtGui import QImage, QPalette, QBrush, QPixmap
from time import sleep


class Menu(QWidget):
    def __init__(self):
        super().__init__()

        self.singlePlayer_btn = QPushButton('SinglePlayer', self)
        self.multiPlayer_btn = QPushButton('MultiPlayer', self)
        self.tournament_btn = QPushButton('Tournament', self)
        self.play_btn = QPushButton('Play', self)  # proverava dal je uneto dva imena, ako jeste, onda pusta u igricu, u suprotnom dalje error message
        self.four_player_btn = QPushButton('4 players', self)
        self.eight_player_btn = QPushButton('8 players', self)

        self.player1_name_textbox = QLineEdit(self)
        self.player2_name_textbox = QLineEdit(self)

        self.player3_name_textbox = QLineEdit(self)
        self.player4_name_textbox = QLineEdit(self)
        self.player5_name_textbox = QLineEdit(self)
        self.player6_name_textbox = QLineEdit(self)
        self.player7_name_textbox = QLineEdit(self)
        self.player8_name_textbox = QLineEdit(self)

        self.player1_yellow_pacman_label = QLabel(self)
        self.player2_orange_pacman_label = QLabel(self)

        self.player3_red_pacman_label = QLabel(self)
        self.player4_pink_pacman_label = QLabel(self)
        self.player5_green_pacman_label = QLabel(self)
        self.player6_blue_pacman_label = QLabel(self)
        self.player7_rose_pacman_label = QLabel(self)
        self.player8_gray_pacman_label = QLabel(self)

        self.init_UI()

    def init_UI(self):
        self.setWindowTitle('Welcome to the game')
        self.setFixedSize(800, 600)
        self.oImage = QImage("images/GameCoverBackground.png")
        self.palette = QPalette()
        self.palette.setBrush(QPalette.Window, QBrush(self.oImage))
        self.setPalette(self.palette)

        self.singlePlayer_btn.setToolTip('Single player mode')
        self.singlePlayer_btn.move(200, 100)
        self.singlePlayer_btn.resize(400, 100)
        self.singlePlayer_btn.setStyleSheet("background-color: blue;""font: 25pt Comic Sans MS;""color: white;""border-radius: 20px;")
        self.singlePlayer_btn.clicked.connect(self.on_click1)

        self.multiPlayer_btn.setToolTip('Multi player mode')
        self.multiPlayer_btn.move(200, 240)
        self.multiPlayer_btn.resize(400, 100)
        self.multiPlayer_btn.setStyleSheet("background-color: red;""font: 25pt Comic Sans MS;""color: white;""border-radius: 20px;")
        self.multiPlayer_btn.clicked.connect(self.on_click2)

        self.tournament_btn.setToolTip('Tournament mode')
        self.tournament_btn.move(200, 380)
        self.tournament_btn.resize(400, 100)
        self.tournament_btn.setStyleSheet("background-color: BurlyWood;""font: 25pt Comic Sans MS;""color: white;""border-radius: 20px;")
        self.tournament_btn.clicked.connect(self.on_click3)

        self.play_btn.setHidden(True)
        self.play_btn.move(500, 245)
        self.play_btn.resize(100, 65)
        self.play_btn.setStyleSheet("background-color: green;""font: 25pt Comic Sans MS;""color: white;""border-radius: 20px;")
        self.play_btn.clicked.connect(self.on_click_check_multiplayer_for_names)

        self.four_player_btn.setHidden(True)
        self.four_player_btn.setToolTip('Truth')
        self.four_player_btn.move(180, 230)
        self.four_player_btn.resize(200, 55)
        self.four_player_btn.setStyleSheet("background-color: red;""font: 25pt Comic Sans MS;""color: white;""border-radius: 25px;")
        self.four_player_btn.clicked.connect(self.four_player_mode)

        self.eight_player_btn.setHidden(True)
        self.eight_player_btn.setToolTip('Illusion')
        self.eight_player_btn.move(420, 230)
        self.eight_player_btn.resize(200, 55)
        self.eight_player_btn.setStyleSheet("background-color: blue;""font: 25pt Comic Sans MS;""color: white;""border-radius: 25px;")
        self.eight_player_btn.clicked.connect(self.eight_player_mode)

        self.player1_name_textbox.move(210,230)
        self.player1_name_textbox.resize(240,40)
        self.player1_name_textbox.setHidden(True)
        self.player1_name_textbox.setStyleSheet("background-color: white;""font: 25pt Comic Sans MS;""color: black;""border-radius: 20px;")
        self.player1_name_textbox.setText(' ')

        self.player2_name_textbox.move(210, 280)
        self.player2_name_textbox.resize(240, 40)
        self.player2_name_textbox.setHidden(True)
        self.player2_name_textbox.setStyleSheet("background-color: white;""font: 25pt Comic Sans MS;""color: black;""border-radius: 20px;")
        self.player2_name_textbox.setText(' ')

        self.player3_name_textbox.move(210, 280)
        self.player3_name_textbox.resize(240, 40)
        self.player3_name_textbox.setHidden(True)
        self.player3_name_textbox.setStyleSheet(
            "background-color: white;""font: 25pt Comic Sans MS;""color: black;""border-radius: 20px;")
        self.player3_name_textbox.setText(' ')

        self.player4_name_textbox.move(210, 280)
        self.player4_name_textbox.resize(240, 40)
        self.player4_name_textbox.setHidden(True)
        self.player4_name_textbox.setStyleSheet(
            "background-color: white;""font: 25pt Comic Sans MS;""color: black;""border-radius: 20px;")
        self.player4_name_textbox.setText(' ')

        self.player5_name_textbox.move(210, 280)
        self.player5_name_textbox.resize(240, 40)
        self.player5_name_textbox.setHidden(True)
        self.player5_name_textbox.setStyleSheet(
            "background-color: white;""font: 25pt Comic Sans MS;""color: black;""border-radius: 20px;")
        self.player5_name_textbox.setText(' ')

        self.player6_name_textbox.move(210, 280)
        self.player6_name_textbox.resize(240, 40)
        self.player6_name_textbox.setHidden(True)
        self.player6_name_textbox.setStyleSheet(
            "background-color: white;""font: 25pt Comic Sans MS;""color: black;""border-radius: 20px;")
        self.player6_name_textbox.setText(' ')

        self.player7_name_textbox.move(210, 280)
        self.player7_name_textbox.resize(240, 40)
        self.player7_name_textbox.setHidden(True)
        self.player7_name_textbox.setStyleSheet(
            "background-color: white;""font: 25pt Comic Sans MS;""color: black;""border-radius: 20px;")
        self.player7_name_textbox.setText(' ')

        self.player8_name_textbox.move(210, 280)
        self.player8_name_textbox.resize(240, 40)
        self.player8_name_textbox.setHidden(True)
        self.player8_name_textbox.setStyleSheet(
            "background-color: white;""font: 25pt Comic Sans MS;""color: black;""border-radius: 20px;")
        self.player8_name_textbox.setText(' ')

        self.player1_yellow_pacman_label.setPixmap(QPixmap('images/PacManRightEat1.png'))
        self.player1_yellow_pacman_label.setHidden(True)
        self.player1_yellow_pacman_label.resize(40,40)
        self.player1_yellow_pacman_label.move(160,230)

        self.player2_orange_pacman_label.setPixmap(QPixmap('images/PacManRightEat2.png'))
        self.player2_orange_pacman_label.setHidden(True)
        self.player2_orange_pacman_label.resize(40, 40)
        self.player2_orange_pacman_label.move(160, 280)

        self.player3_red_pacman_label.setPixmap(QPixmap('images/PacManRightEat3.png'))
        self.player3_red_pacman_label.setHidden(True)
        self.player3_red_pacman_label.resize(40, 40)
        self.player3_red_pacman_label.move(160, 330)

        self.player4_pink_pacman_label.setPixmap(QPixmap('images/PacManRightEat4.png'))
        self.player4_pink_pacman_label.setHidden(True)
        self.player4_pink_pacman_label.resize(40, 40)
        self.player4_pink_pacman_label.move(160, 380)

        self.player5_green_pacman_label.setPixmap(QPixmap('images/PacManRightEat5.png'))
        self.player5_green_pacman_label.setHidden(True)
        self.player5_green_pacman_label.resize(40, 40)
        self.player5_green_pacman_label.move(480, 380)

        self.player6_blue_pacman_label.setPixmap(QPixmap('images/PacManRightEat6.png'))
        self.player6_blue_pacman_label.setHidden(True)
        self.player6_blue_pacman_label.resize(40, 40)
        self.player6_blue_pacman_label.move(480, 430)

        self.player7_rose_pacman_label.setPixmap(QPixmap('images/PacManRightEat7.png'))
        self.player7_rose_pacman_label.setHidden(True)
        self.player7_rose_pacman_label.resize(40, 40)
        self.player7_rose_pacman_label.move(480, 480)

        self.player8_gray_pacman_label.setPixmap(QPixmap('images/PacManRightEat8.png'))
        self.player8_gray_pacman_label.setHidden(True)
        self.player8_gray_pacman_label.resize(40, 40)
        self.player8_gray_pacman_label.move(480, 530)


    @pyqtSlot()
    def on_click1(self):
        #kreiraj mainWindow sa jednim playerom
        self.mw = MainWindow([(1, 'DjuroTelevizor')])
        self.mw.show()
        self.close()

    @pyqtSlot()
    def on_click2(self): # 2 player
        self.oImage = QImage("images/InitialForMultiplayer.png")
        self.palette.setBrush(QPalette.Window, QBrush(self.oImage))
        self.setPalette(self.palette)
        self.singlePlayer_btn.setHidden(True)
        self.multiPlayer_btn.setHidden(True)
        self.tournament_btn.setHidden(True)
        self.play_btn.setHidden(False)
        self.player1_name_textbox.setHidden(False)
        self.player2_name_textbox.setHidden(False)
        self.player1_yellow_pacman_label.setHidden(False)
        self.player2_orange_pacman_label.setHidden(False)

    @pyqtSlot()
    def on_click3(self): # 4 or 8 # InitialForTournament.png
        self.oImage = QImage("images/InitialForTournament.png")
        self.palette.setBrush(QPalette.Window, QBrush(self.oImage))
        self.setPalette(self.palette)
        self.singlePlayer_btn.setHidden(True)
        self.multiPlayer_btn.setHidden(True)
        self.tournament_btn.setHidden(True)
        self.four_player_btn.setHidden(False)
        self.eight_player_btn.setHidden(False)
        self.play_btn.disconnect()

    @pyqtSlot()
    def on_click_check_multiplayer_for_names(self):
        player1_name = self.player1_name_textbox.text().strip()
        player2_name = self.player2_name_textbox.text().strip()
        if player1_name == "" and player2_name == "":
            self.oImage = QImage("images/BothNamesMissingMultiplayer.png")
            self.palette.setBrush(QPalette.Window, QBrush(self.oImage))
            self.setPalette(self.palette)
        elif player1_name == "":
            self.oImage = QImage("images/Player1MissingMultiplayer.png")
            self.palette.setBrush(QPalette.Window, QBrush(self.oImage))
            self.setPalette(self.palette)
        elif player2_name == "":
            self.oImage = QImage("images/Player2MissingMultiplayer.png")
            self.palette.setBrush(QPalette.Window, QBrush(self.oImage))
            self.setPalette(self.palette)
        else:
            self.mw = MainWindow([(1, player1_name), (2, player2_name)]) # prosledi imena kao argumente
            self.mw.show()
            self.close()

    @pyqtSlot()
    def on_click_check_tournament_names_for_four(self):
        player1_name = self.player1_name_textbox.text().strip()
        player2_name = self.player2_name_textbox.text().strip()
        player3_name = self.player3_name_textbox.text().strip()
        player4_name = self.player4_name_textbox.text().strip()
        if player1_name == "" or player2_name == "" or player3_name == "" or player4_name == "":
            self.oImage = QImage("images/TournamentFail.png")
            self.palette.setBrush(QPalette.Window, QBrush(self.oImage))
            self.setPalette(self.palette)
        else:
            self.mw = MainWindow([(1, player1_name),(2, player2_name),(3, player3_name),(4, player4_name)])  # prosledi imena kao argumente
            self.mw.show()
            self.close()

    @pyqtSlot()
    def on_click_check_tournament_names_for_eight(self):
        player1_name = self.player1_name_textbox.text().strip()
        player2_name = self.player2_name_textbox.text().strip()
        player3_name = self.player3_name_textbox.text().strip()
        player4_name = self.player4_name_textbox.text().strip()
        player5_name = self.player5_name_textbox.text().strip()
        player6_name = self.player6_name_textbox.text().strip()
        player7_name = self.player7_name_textbox.text().strip()
        player8_name = self.player8_name_textbox.text().strip()
        if player1_name == "" or player2_name == "" or player3_name == "" or player4_name == "" or player5_name == "" or player6_name == "" or player7_name == "" or player8_name == "":
            self.oImage = QImage("images/EightPlayerMissingNames.png")
            self.palette.setBrush(QPalette.Window, QBrush(self.oImage))
            self.setPalette(self.palette)
        else:
            self.mw = MainWindow([(1, player1_name),(2, player2_name),(3, player3_name),(4, player4_name),(5, player5_name),(6, player6_name),(7, player7_name),(8, player8_name)])  # prosledi imena kao argumente
            self.mw.show()
            self.close()

    @pyqtSlot()
    def four_player_mode(self):
        self.move_name_inputs(4)

    @pyqtSlot()
    def eight_player_mode(self):
        self.move_name_inputs(8)

    def move_name_inputs(self, how_much_to_show: int): # FillTheNamesTournament.png TournamentFail.png # EightPlayerMissingNames.png
        self.four_player_btn.setHidden(True)
        self.eight_player_btn.setHidden(True)
        self.play_btn.setHidden(False)

        self.oImage = QImage("images/FillTheNamesTournament.png")
        self.palette.setBrush(QPalette.Window, QBrush(self.oImage))
        self.setPalette(self.palette)

        if how_much_to_show == 4 or how_much_to_show == 8:
            if how_much_to_show != 8:
                self.play_btn.clicked.connect(self.on_click_check_tournament_names_for_four)
            self.player1_name_textbox.setHidden(False)
            self.player2_name_textbox.setHidden(False)
            self.player3_name_textbox.setHidden(False)
            self.player4_name_textbox.setHidden(False)
            self.player1_yellow_pacman_label.setHidden(False)
            self.player2_orange_pacman_label.setHidden(False)
            self.player3_red_pacman_label.setHidden(False)
            self.player4_pink_pacman_label.setHidden(False)

            self.player1_name_textbox.move(210, 230)
            self.player2_name_textbox.move(210, 280)
            self.player3_name_textbox.move(210, 330)
            self.player4_name_textbox.move(210, 380)
        if how_much_to_show == 8:
            self.play_btn.clicked.connect(self.on_click_check_tournament_names_for_eight)
            self.player5_name_textbox.setHidden(False)
            self.player6_name_textbox.setHidden(False)
            self.player7_name_textbox.setHidden(False)
            self.player8_name_textbox.setHidden(False)
            self.player5_green_pacman_label.setHidden(False)
            self.player6_blue_pacman_label.setHidden(False)
            self.player7_rose_pacman_label.setHidden(False)
            self.player8_gray_pacman_label.setHidden(False)

            self.player5_name_textbox.move(530, 380)
            self.player6_name_textbox.move(530, 430)
            self.player7_name_textbox.move(530, 480)
            self.player8_name_textbox.move(530, 530)

    def center_window(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)