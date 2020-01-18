from PyQt5.QtWidgets import QWidget, QPushButton, QDesktopWidget, QLineEdit, QLabel
from PyQt5.QtCore import pyqtSlot, QSize
from main_window import MainWindow
from PyQt5.QtGui import QImage, QPalette, QBrush, QPixmap, QIcon
from functools import partial


class Menu(QWidget):
    def __init__(self):
        super().__init__()

        self.singlePlayer_btn = QPushButton('SinglePlayer', self)
        self.multiPlayer_btn = QPushButton('MultiPlayer', self)
        self.tournament_btn = QPushButton('Tournament', self)
        self.play_btn = QPushButton('Play', self)  # proverava dal je uneto dva imena, ako jeste, onda pusta u igricu, u suprotnom dalje error message
        self.four_player_btn = QPushButton('4 players', self)
        self.eight_player_btn = QPushButton('8 players', self)
        self.back_btn = QPushButton('Go Back', self, objectName="BackButton")

        self.yellow_pacman_button = QPushButton('',self)
        self.orange_pacman_button = QPushButton('',self)
        self.red_pacman_button = QPushButton('',self)
        self.pink_pacman_button = QPushButton('',self)
        self.green_pacman_button = QPushButton('',self)
        self.blue_pacman_button = QPushButton('',self)
        self.rose_pacman_button = QPushButton('',self)
        self.gray_pacman_button = QPushButton('',self)

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

        StyleSheet = '''
        QPushButton#BackButton {
            background-color: aqua;
            border-radius: 20px;      
            font: 15pt Comic Sans MS;
        }

        QPushButton#BackButton:hover {
            background-color: #64b5f6;
            color: #fff;
        }

        QPushButton#BackButton:pressed {
            background-color: #bbdefb;
        }
        '''
        self.back_btn.move(600, 10)
        self.back_btn.resize(100, 40)
        self.back_btn.setStyleSheet(StyleSheet)
        self.back_btn.clicked.connect(self.go_back)
        self.back_btn.setHidden(True)

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

        self.yellow_pacman_button.setHidden(True)
        self.yellow_pacman_button.clicked.connect(partial(self.choose_pacman_button, "yellow"))
        self.yellow_pacman_button.setIcon(QIcon('images/PacManRightEat1.png'))
        self.yellow_pacman_button.setIconSize(QSize(40, 40))
        self.yellow_pacman_button.move(380,200)
        self.yellow_pacman_button.setStyleSheet("background:transparent")

        self.orange_pacman_button.setHidden(True)
        self.orange_pacman_button.clicked.connect(partial(self.choose_pacman_button, "orange"))
        self.orange_pacman_button.setIcon(QIcon('images/PacManRightEat2.png'))
        self.orange_pacman_button.setIconSize(QSize(40, 40))
        self.orange_pacman_button.move(310, 230)
        self.orange_pacman_button.setStyleSheet("background:transparent")

        self.red_pacman_button.setHidden(True)
        self.red_pacman_button.clicked.connect(partial(self.choose_pacman_button, "red"))
        self.red_pacman_button.setIcon(QIcon('images/PacManRightEat3.png'))
        self.red_pacman_button.setIconSize(QSize(40, 40))
        self.red_pacman_button.move(450, 230)
        self.red_pacman_button.setStyleSheet("background:transparent")

        self.pink_pacman_button.setHidden(True)
        self.pink_pacman_button.clicked.connect(partial(self.choose_pacman_button, "pink"))
        self.pink_pacman_button.setIcon(QIcon('images/PacManRightEat4.png'))
        self.pink_pacman_button.setIconSize(QSize(40, 40))
        self.pink_pacman_button.move(280, 300)
        self.pink_pacman_button.setStyleSheet("background:transparent")

        self.green_pacman_button.setHidden(True)
        self.green_pacman_button.clicked.connect(partial(self.choose_pacman_button, "green"))
        self.green_pacman_button.setIcon(QIcon('images/PacManRightEat5.png'))
        self.green_pacman_button.setIconSize(QSize(40, 40))
        self.green_pacman_button.move(480, 300)
        self.green_pacman_button.setStyleSheet("background:transparent")

        self.blue_pacman_button.setHidden(True)
        self.blue_pacman_button.clicked.connect(partial(self.choose_pacman_button, "blue"))
        self.blue_pacman_button.setIcon(QIcon('images/PacManRightEat6.png'))
        self.blue_pacman_button.setIconSize(QSize(40, 40))
        self.blue_pacman_button.move(310, 370)
        self.blue_pacman_button.setStyleSheet("background:transparent")

        self.rose_pacman_button.setHidden(True)
        self.rose_pacman_button.clicked.connect(partial(self.choose_pacman_button, "rose"))
        self.rose_pacman_button.setIcon(QIcon('images/PacManRightEat7.png'))
        self.rose_pacman_button.setIconSize(QSize(40, 40))
        self.rose_pacman_button.move(450, 370)
        self.rose_pacman_button.setStyleSheet("background:transparent")

        self.gray_pacman_button.setHidden(True)
        self.gray_pacman_button.clicked.connect(partial(self.choose_pacman_button, "gray"))
        self.gray_pacman_button.setIcon(QIcon('images/PacManRightEat8.png'))
        self.gray_pacman_button.setIconSize(QSize(40, 40))
        self.gray_pacman_button.move(380, 400)
        self.gray_pacman_button.setStyleSheet("background:transparent")

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
    def on_click1(self): # SingleplayerInitial.png
        self.oImage = QImage("images/SingleplayerInitial.png")
        self.palette.setBrush(QPalette.Window, QBrush(self.oImage))
        self.setPalette(self.palette)
        self.back_btn.setHidden(False)
        self.singlePlayer_btn.setHidden(True)
        self.multiPlayer_btn.setHidden(True)
        self.tournament_btn.setHidden(True)
        self.yellow_pacman_button.setHidden(False)
        self.orange_pacman_button.setHidden(False)
        self.red_pacman_button.setHidden(False)
        self.pink_pacman_button.setHidden(False)
        self.green_pacman_button.setHidden(False)
        self.blue_pacman_button.setHidden(False)
        self.rose_pacman_button.setHidden(False)
        self.gray_pacman_button.setHidden(False)


    @pyqtSlot()
    def go_back(self):
        new_window = Menu()
        self.close()
        new_window.show()

    @pyqtSlot()
    def choose_pacman_button(self, button_argument):
        if button_argument == "yellow":
            self.mw = MainWindow([(1, '')], None)
        elif button_argument == "orange":
            self.mw = MainWindow([(2, '')], None)
        elif button_argument == "red":
            self.mw = MainWindow([(3, '')], None)
        elif button_argument == "pink":
            self.mw = MainWindow([(4, '')], None)
        elif button_argument == "green":
            self.mw = MainWindow([(5, '')], None)
        elif button_argument == "blue":
            self.mw = MainWindow([(6, '')], None)
        elif button_argument == "rose":
            self.mw = MainWindow([(7, '')], None)
        elif button_argument == "gray":
            self.mw = MainWindow([(8, '')], None)
        self.mw.show()
        self.close()

    @pyqtSlot()
    def on_click2(self): # 2 player
        self.oImage = QImage("images/InitialForMultiplayer.png")
        self.palette.setBrush(QPalette.Window, QBrush(self.oImage))
        self.setPalette(self.palette)
        self.back_btn.setHidden(False)
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
        self.back_btn.setHidden(False)
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
            self.mw = MainWindow([(1, player1_name), (2, player2_name)], None) # prosledi imena kao argumente
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
            self.tw = TournamentWindow([player1_name, player2_name, player3_name, player4_name])
            self.tw.show()
            self.mw = MainWindow([(1, player1_name),(2, player2_name),(3, player3_name),(4, player4_name)], self.tw)  # prosledi imena kao argumente
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
            self.tw = TournamentWindow([player1_name, player2_name, player3_name, player4_name,player5_name, player6_name, player7_name, player8_name])
            self.tw.show()
            self.mw = MainWindow([(1, player1_name),(2, player2_name),(3, player3_name),(4, player4_name),(5, player5_name),(6, player6_name),(7, player7_name),(8, player8_name)], self.tw)  # prosledi imena kao argumente
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


class TournamentWindow(QWidget): # 800, 640
    def __init__(self, list_of_names):
        super().__init__()
        self.player_names = list_of_names
        self.tournament_type = len(list_of_names)
        self.finished_round = 0

        self.init_UI()
        self.center_window()

    def init_UI(self):
        self.setWindowTitle('Tournament table')
        self.setFixedSize(800, 600)
        self.oImage = QImage("images/FourTornamentInitial.png")

        self.field1_for_name = QLabel(self.player_names[0].capitalize(),self)
        self.field1_for_name.move(60,235)
        self.field1_for_name.setStyleSheet("font: 16pt Comic Sans MS; color: white")
        self.field2_for_name = QLabel(self.player_names[1].capitalize(),self)
        self.field2_for_name.move(60, 390)
        self.field2_for_name.setStyleSheet("font: 16pt Comic Sans MS; color: white")
        self.field3_for_name = QLabel(self.player_names[2].capitalize(),self)
        self.field3_for_name.move(650, 235)
        self.field3_for_name.setStyleSheet("font: 16pt Comic Sans MS; color: white")
        self.field4_for_name = QLabel(self.player_names[3].capitalize(),self)
        self.field4_for_name.move(650, 390)
        self.field4_for_name.setStyleSheet("font: 16pt Comic Sans MS; color: white")

        self.field5_for_name = QLabel(self)
        self.field5_for_name.move(268, 312)
        self.field5_for_name.setStyleSheet("font: 16pt Comic Sans MS; color: white")
        self.field5_for_name.resize(200,40)

        self.field6_for_name = QLabel(self)
        self.field6_for_name.move(441, 313)
        self.field6_for_name.setStyleSheet("font: 16pt Comic Sans MS; color: white")
        self.field6_for_name.resize(200, 40)

        self.field7_for_name = QLabel(self)
        self.field7_for_name.move(339, 389)
        self.field7_for_name.setStyleSheet("font: 16pt Comic Sans MS; color: white")
        self.field7_for_name.resize(200, 40)

        self.pacman_icon1 = QLabel(self)
        self.pacman_icon1.move(225, 311)
        self.pacman_icon1.resize(40,40)

        self.pacman_icon2 = QLabel(self)
        self.pacman_icon2.move(541, 311)
        self.pacman_icon2.resize(40, 40)

        self.pacman_icon3 = QLabel(self)
        self.pacman_icon3.move(382, 461)
        self.pacman_icon3.resize(40, 40)

        if self.tournament_type == 8:
            self.oImage = QImage("images/EightTornamentInitial.png")
            self.field1_for_name.setStyleSheet("font: 14pt Comic Sans MS; color: white")
            self.field1_for_name.move(45, 155)
            self.field1_for_name.resize(100, 100)
            self.field2_for_name.setStyleSheet("font: 14pt Comic Sans MS; color: white")
            self.field2_for_name.move(45, 322)
            self.field3_for_name.setStyleSheet("font: 14pt Comic Sans MS; color: white")
            self.field3_for_name.move(45, 370)
            self.field4_for_name.setStyleSheet("font: 14pt Comic Sans MS; color: white")
            self.field4_for_name.move(45, 502)
            self.field5_for_name.setText(self.player_names[4].capitalize())
            self.field5_for_name.setStyleSheet("font: 14pt Comic Sans MS; color: white")
            self.field5_for_name.move(682, 187)
            self.field6_for_name.setText(self.player_names[5].capitalize())
            self.field6_for_name.setStyleSheet("font: 14pt Comic Sans MS; color: white")
            self.field6_for_name.move(682, 318)
            self.field7_for_name.setText(self.player_names[6].capitalize())
            self.field7_for_name.setStyleSheet("font: 14pt Comic Sans MS; color: white")
            self.field7_for_name.move(682, 366)
            self.field8_for_name = QLabel(self.player_names[7].capitalize(), self)
            self.field8_for_name.setStyleSheet("font: 14pt Comic Sans MS; color: white")
            self.field8_for_name.move(682, 502)

            self.pacman_icon1.move(187, 252)
            self.field9_for_name = QLabel(self)
            self.field9_for_name.setStyleSheet("font: 14pt Comic Sans MS; color: white")
            self.field9_for_name.move(223,251)
            self.field9_for_name.resize(200, 40)

            self.pacman_icon2.move(187, 432)
            self.field10_for_name = QLabel(self)
            self.field10_for_name.setStyleSheet("font: 14pt Comic Sans MS; color: white")
            self.field10_for_name.move(223,431)
            self.field10_for_name.resize(200, 40)

            self.pacman_icon3.move(588, 252)
            self.field11_for_name = QLabel( self)
            self.field11_for_name.setStyleSheet("font: 14pt Comic Sans MS; color: white")
            self.field11_for_name.move(506, 251)
            self.field11_for_name.resize(200, 40)

            self.pacman_icon4 = QLabel(self)
            self.pacman_icon4.move(586, 432)
            self.pacman_icon4.resize(40, 40)
            self.field12_for_name = QLabel(self)
            self.field12_for_name.setStyleSheet("font: 14pt Comic Sans MS; color: white")
            self.field12_for_name.move(506, 431)
            self.field12_for_name.resize(200, 40)

            self.pacman_icon5 = QLabel(self) #345 26
            self.pacman_icon5.move(340, 320)
            self.pacman_icon5.resize(40, 40)
            self.field13_for_name = QLabel(self)
            self.field13_for_name.setStyleSheet("font: 14pt Comic Sans MS; color: white")
            self.field13_for_name.move(379, 318)
            self.field13_for_name.resize(200, 40)

            self.pacman_icon6 = QLabel(self)
            self.pacman_icon6.move(433, 370)
            self.pacman_icon6.resize(40, 40)
            self.field14_for_name = QLabel(self)
            self.field14_for_name.setStyleSheet("font: 14pt Comic Sans MS; color: white")
            self.field14_for_name.move(355, 369)
            self.field14_for_name.resize(200, 40)

            self.pacman_icon7 = QLabel(self)
            self.pacman_icon7.move(386, 531)
            self.pacman_icon7.resize(40, 40)
            self.field15_for_name = QLabel(self)
            self.field15_for_name.setStyleSheet("font: 14pt Comic Sans MS; color: white")
            self.field15_for_name.move(356, 460)
            self.field15_for_name.resize(200, 40)

        self.palette = QPalette()
        self.palette.setBrush(QPalette.Window, QBrush(self.oImage))
        self.setPalette(self.palette)

    def center_window(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(((screen.width() - size.width()) / 2),
                  ((screen.height() - size.height()) / 2)-40)

    def round_done(self, winner_player_id, winner_player_name):
        # Winner matricu napravi!
        self.finished_round += 1
        if self.finished_round == 1:
            if self.tournament_type == 4:
                self.field5_for_name.setText(winner_player_name.capitalize()) #
                self.pacman_icon1.setPixmap(QPixmap('images/TournamentFourPlayer'+str(winner_player_id)+'.png'))
            elif self.tournament_type == 8:
                self.field9_for_name.setText(winner_player_name.capitalize())
                self.pacman_icon1.setPixmap(QPixmap('images/TournamentEightPlayer'+str(winner_player_id)+'.png'))
        elif self.finished_round == 2:
            if self.tournament_type == 4:
                self.field6_for_name.setText(winner_player_name.capitalize())  #
                self.pacman_icon2.setPixmap(QPixmap('images/TournamentFourPlayer' + str(winner_player_id) + '.png'))
            elif self.tournament_type == 8:
                self.field10_for_name.setText(winner_player_name.capitalize())
                self.pacman_icon2.setPixmap(QPixmap('images/TournamentEightPlayer' + str(winner_player_id) + '.png'))
        elif self.finished_round == 3:
            if self.tournament_type == 4:
                self.field7_for_name.setText(winner_player_name.capitalize())  #
                self.pacman_icon3.setPixmap(QPixmap('images/PacManRightEat'+ str(winner_player_id) + '.png'))
            elif self.tournament_type == 8:
                self.field11_for_name.setText(winner_player_name.capitalize())
                self.pacman_icon3.setPixmap(QPixmap('images/TournamentEightPlayer' + str(winner_player_id) + '.png'))
        elif self.finished_round == 4 and self.tournament_type == 8:
            self.field12_for_name.setText(winner_player_name.capitalize())
            self.pacman_icon4.setPixmap(QPixmap('images/TournamentEightPlayer' + str(winner_player_id) + '.png'))
        elif self.finished_round == 5 and self.tournament_type == 8:
            self.field13_for_name.setText(winner_player_name.capitalize())
            self.pacman_icon5.setPixmap(QPixmap('images/TournamentEightPlayer' + str(winner_player_id) + '.png'))
        elif self.finished_round == 6 and self.tournament_type == 8:
            self.field14_for_name.setText(winner_player_name.capitalize())
            self.pacman_icon6.setPixmap(QPixmap('images/TournamentEightPlayer' + str(winner_player_id) + '.png'))
        elif self.finished_round == 7 and self.tournament_type == 8:
            self.field15_for_name.setText(winner_player_name.capitalize())
            self.pacman_icon7.setPixmap(QPixmap('images/PacManRightEat' + str(winner_player_id) + '.png'))