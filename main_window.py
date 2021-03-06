from PyQt5.QtWidgets import (QMainWindow, QLabel, QDesktopWidget, QFrame, QPushButton)
from PyQt5.QtGui import (QPainter, QPixmap, QIcon, QMovie, QTextDocument)
from PyQt5.QtCore import Qt, QThreadPool, pyqtSlot, QCoreApplication
import player
import enemy
from time import sleep
from threading import Thread
from multiprocessing import Process
from key_notifier import KeyNotifier
import winsound

"""
centralni widget u MainWindow je mapa(matrica 16x16) = klasa Board
"""


class MainWindow(QMainWindow):

    def __init__(self, list_of_names, tournament_window):
        super().__init__()

        self.width = 800
        self.height = 640

        self.map = Board(self)
        self.list_of_player_names = list_of_names
        self.play_mode = len(list_of_names)  # 1 - Singleplayer, 2 - Multiplayer, 4 - Tornament w 4 players, 8- Tournament w 8 players. Dodaj 0
        self.tournament_window = tournament_window  # Posle svakog turnira (tj runde) treba pozvati metodu self.tournament_window.round_done(winner_id, winner_name) da se azurira prozor

        # Labele
        self.blue_ghost = QLabel(self)
        self.orange_ghost = QLabel(self)
        self.red_ghost = QLabel(self)
        self.yellow_ghost = QLabel(self)
        self.deus_ex_feedback_label = QLabel(self)
        self.deus_ex_feedback_label2 = QLabel(self)
        self.player2 = None

        self.label_super_power = QLabel(self)
        self.niz_lokacija_special_power = [(2, 5), (18, 1), (6, 12), (2, 5), (10, 10), (18, 8)]
        self.movie = QMovie('images/SpecialPowers.gif')
        self.label_super_power.move(self.niz_lokacija_special_power[0][0] * 40,
                                    self.niz_lokacija_special_power[0][1] * 40)
        self.label_super_power.resize(40, 40)
        self.label_super_power.setMovie(self.movie)
        self.movie.start()
        self.map.board[self.niz_lokacija_special_power[0][1]][self.niz_lokacija_special_power[0][0]] = 4

        self.title_label = QLabel('PacMan', self)
        self.countdown_label = QLabel(self)
        self.score_label_player = QLabel(self)  # Samo ce im se menjati imena sa .setText(self.player1.player_name+' Score: ', self) kada se menjaju igraci
        self.player1_name_label = QLabel(self)
        self.player2_name_label = QLabel(self)
        self.image_label_for_winner_or_next_player = QLabel(self)
        self.winner_label = QLabel(self)
        self.next_players_label = QLabel(self)

        self.restart_btn = QPushButton('Play', self)
        self.restart_btn_pushed = False

        special_power_thread = Thread(target=self.changeSpecialPowerLocation, args=[30,12])  # Thread koji menja pozicije, svake 30s generise superPower, i ostavlja ju je vidljivo 12s
        special_power_thread.daemon = True  # Da se thread gasi zajedno sa gasenjem glavnog threada (posle zatvaranja prozora)
        special_power_thread.start()

        self.instantiate_players_from_list(self.list_of_player_names)

        self.init_ui()
        self.drawPlayer()
        self.draw_ghosts()
        self.initPlayerScore()
        self.start_enemies()

        self.key_notifier = KeyNotifier()
        self.key_notifier.key_signal.connect(self.__update_position__)
        self.key_notifier.start()

        self.show()

##################################################################################################
    def init_ui(self):
        self.setWindowTitle('Pac-Man')
        self.setFixedWidth(self.width)
        self.setFixedHeight(self.height)
        self.setWindowIcon(QIcon('images/PacManRightEat1.png'))

        self.center_window()
        self.setCentralWidget(self.map)

        self.image_label_for_winner_or_next_player.move(35,160)
        self.image_label_for_winner_or_next_player.resize(730,291)
        self.image_label_for_winner_or_next_player.setHidden(True)
        self.deus_ex_feedback_label.setHidden(True)
        self.deus_ex_feedback_label.move(0,40)
        self.deus_ex_feedback_label.resize(40,40)

        self.deus_ex_feedback_label2.setHidden(True)
        self.deus_ex_feedback_label2.move(760, 40)
        self.deus_ex_feedback_label2.resize(40, 40)

        if self.play_mode == 1:  # singleplayer
            player_id, player_name = self.list_of_player_names[0]
            self.score_label_player.move(5, 5)
            self.score_label_player.setStyleSheet("font: 20pt Comic Sans MS; color: white")
            self.score_label_player.resize(150, 30)
            self.score_label_player.setText('Score: ')

            self.player1_name_label.resize(150, 30)
            self.player1_name_label.move(15, 600)
            self.player1_name_label.setStyleSheet("font: 15pt Comic Sans MS; color: red")
            self.player1_name_label.setText(str(player_name))

            self.label_for_player_lifes.setPixmap(QPixmap('images/TwoLife' + str(self.player.player_id) + '.png'))
            self.label_for_player_lifes.move(685, 0)
            self.label_for_player_lifes.resize(80, 40)


        elif self.play_mode in (2, 4, 8):
            player_id, player_name = self.list_of_player_names[0]
            self.score_label_player.move(5, 5)
            self.score_label_player.setStyleSheet("font: 18pt Comic Sans MS; color: white")
            self.score_label_player.resize(150, 30)
            self.score_label_player.setText('Score: ')

            self.score_label_player2 = QLabel(self)
            self.score_label_player2.move(510, 5)
            self.score_label_player2.setStyleSheet("font: 18pt Comic Sans MS; color: white")
            self.score_label_player2.resize(150, 30)
            self.score_label_player2.setText('Score: ')

            self.player1_name_label.resize(150, 30)
            self.player1_name_label.move(15, 600)
            self.player1_name_label.setStyleSheet("font: 15pt Comic Sans MS; color: red")
            self.player1_name_label.setText(str(player_name).capitalize())

            player_id2, player2_name = self.list_of_player_names[1]
            self.player2_name_label.resize(150, 30)
            self.player2_name_label.move(700, 600)
            self.player2_name_label.setStyleSheet("font: 15pt Comic Sans MS; color: aqua")
            self.player2_name_label.setText(str(player2_name).capitalize())

            self.label_for_coin_display2 = QLabel(self)
            self.label_for_coin_display2.setPixmap(QPixmap("images/ResultCoins.png"))
            self.label_for_coin_display2.move(615, 5)
            self.label_for_coin_display2.resize(30, 30)

            self.label_for_player_lifes.setPixmap(QPixmap('images/TwoLife' + str(self.player.player_id) + '.png'))
            self.label_for_player_lifes.move(210, 0)
            self.label_for_player_lifes.resize(80, 40)

            self.label_for_player2_lifes.setPixmap(QPixmap('images/TwoLife' + str(self.player2.player_id) + '.png'))
            self.label_for_player2_lifes.move(720, 0)
            self.label_for_player2_lifes.resize(80, 40)

        self.title_label.setStyleSheet("font: 20pt Comic Sans MS; color: white")
        self.title_label.move(350, 5)
        self.title_label.resize(150, 30)

        self.label_for_coin_display.setPixmap(QPixmap("images/ResultCoins.png"))
        self.label_for_coin_display.move(110, 5)
        self.label_for_coin_display.resize(30, 30)

        self.countdown_label.move(360, 200)
        self.countdown_label.setStyleSheet("font: 120pt Comic Sans MS; color: white")
        self.countdown_label.resize(200, 200)

        self.winner_label.move(180, 20)
        self.winner_label.setStyleSheet("font: 30pt Comic Sans MS; color: white")
        self.winner_label.resize(500, 500)
        self.winner_label.setText('')

        self.next_players_label.move(140, 95)
        self.next_players_label.setStyleSheet("font: 22pt Comic Sans MS; color: green")
        self.next_players_label.resize(700, 500)
        self.next_players_label.setText('')

        self.restart_btn.move(630, 383)
        self.restart_btn.resize(100, 50)
        self.restart_btn.setStyleSheet("font: 30pt Comaic Sans MS; color: white; border: 1px solid black;"
                                       "border-radius: 5px; background-color: BurlyWood;")
        self.restart_btn.setText('Play')
        self.restart_btn.setHidden(True)
        self.restart_btn.clicked.connect(self.on_end_game)

        self.grave_label.resize(40, 40)
        if self.play_mode in (2, 4, 8):
            self.grave_label_for_player2.resize(40, 40)

####################################################################################################

    def do_initial_countdown(self):
        QCoreApplication.processEvents()
        self.player.in_reset = True
        if self.play_mode in (2, 4, 8):
           self.player2.in_reset = True
        self.countdown_label.setText('3')
        sleep(1)
        QCoreApplication.processEvents()
        self.countdown_label.setText('2')
        sleep(1)
        QCoreApplication.processEvents()
        self.countdown_label.move(370, 200)
        self.countdown_label.setText('1')
        sleep(1)

        self.countdown_label.move(360, 200)
        self.countdown_label.setText('')
        QCoreApplication.processEvents()
        self.player.in_reset = False
        if self.play_mode in (2, 4, 8):
          self.player2.in_reset = False

########################### PLAYER FUNCTIONS ###################################################
    def instantiate_players_from_list(self, list_of_names):
        number_of_elements = len(list_of_names)
        if number_of_elements == 1:  # SINGLEPLAYER

            player_id, player_name = list_of_names[0]
            self.player_label = QLabel(self)
            self.label_for_player_score = QLabel(self)
            self.label_for_coin_display = QLabel(self)
            self.label_for_player_lifes = QLabel(self)
            self.grave_label = QLabel(self)
            self.player = player.Player(self.player_label, self.map, self.label_for_player_score,
                                        self.label_for_player_lifes, self.grave_label, (40, 560), player_id,
                                        player_name, 0.07, self.label_super_power,self.deus_ex_feedback_label)

            self.ghost1 = enemy.Enemy(self.red_ghost, self.map, self.player, None, (18 * 40, 1 * 40), 1, self.red_ghost,
                                      (360, 400))  # red ghost
            self.ghost2 = enemy.Enemy(self.orange_ghost, self.map, self.player, None, (1 * 40, 1 * 40), 2,
                                      self.red_ghost, (440, 360))  # orange ghost
            self.ghost3 = enemy.Enemy(self.yellow_ghost, self.map, self.player, None, (1 * 40, 13 * 40), 3,
                                      self.red_ghost, (440, 400))  # yellow ghost
            self.ghost4 = enemy.Enemy(self.blue_ghost, self.map, self.player, None, (18 * 40, 13 * 40), 4,
                                      self.red_ghost, (360, 360))  # blue ghost

        elif number_of_elements in (2, 4, 8):  # MULTIPLAYER ili TOURNAMENT
            player1_id, player1_name = list_of_names[0]
            self.player_label = QLabel(self)
            self.label_for_player_score = QLabel(self)
            self.label_for_coin_display = QLabel(self)
            self.label_for_player_lifes = QLabel(self)
            self.grave_label = QLabel(self)
            self.player = player.Player(self.player_label, self.map, self.label_for_player_score,
                                        self.label_for_player_lifes, self.grave_label, (40, 560), player1_id,
                                        player1_name, 0.07, self.label_super_power,self.deus_ex_feedback_label)

            player2_id, player2_name = list_of_names[1]
            self.player2_label = QLabel(self)
            self.label_for_player2_score = QLabel(self)
            self.label_for_coin_display_player2 = QLabel(self)
            self.label_for_player2_lifes = QLabel(self)
            self.grave_label_for_player2 = QLabel(self)

            self.player2 = player.Player(self.player2_label, self.map, self.label_for_player2_score,self.label_for_player2_lifes, self.grave_label_for_player2, (720, 560),player2_id, player2_name, 0.07, self.label_super_power,self.deus_ex_feedback_label2)
            self.ghost1 = enemy.Enemy(self.red_ghost, self.map, self.player, self.player2, (18 * 40, 1 * 40), 1,
                                      self.red_ghost, (360, 400))  # red ghost
            self.ghost2 = enemy.Enemy(self.orange_ghost, self.map, self.player2, self.player, (1 * 40, 1 * 40), 2,
                                      self.red_ghost, (440, 360))  # orange ghost
            self.ghost3 = enemy.Enemy(self.yellow_ghost, self.map, self.player2, self.player, (1 * 40, 13 * 40), 3,
                                      self.red_ghost, (440, 400))  # yellow ghost
            self.ghost4 = enemy.Enemy(self.blue_ghost, self.map, self.player, self.player2, (18 * 40, 13 * 40), 4,
                                      self.red_ghost, (360, 360))  # blue ghost

    def drawPlayer(self):
        self.player_label.setPixmap(QPixmap("images/PacManUpEat" + str(self.player.player_id) + ".png"))
        self.player_label.resize(40, 40)
        self.player_label.setStyleSheet("background:transparent")
        self.player_label.move(40, 560)

        if self.play_mode in (2, 4, 8):
            self.player2_label.setPixmap(QPixmap("images/PacManUpEat" + str(self.player2.player_id) + ".png"))
            self.player2_label.resize(40, 40)
            self.player2_label.setStyleSheet("background:transparent")
            self.player2_label.move(720, 560)

    def initPlayerScore(self):
        self.label_for_player_score.setText('0')
        self.label_for_player_score.setStyleSheet("font: 19pt Comic Sans MS; color: white")
        self.label_for_player_score.move(135, 5)
        if self.play_mode in (2, 4, 8):
            self.label_for_player2_score.setText('0')
            self.label_for_player2_score.setStyleSheet("font: 19pt Comic Sans MS; color: white")
            self.label_for_player2_score.move(640, 5)

    def keyPressEvent(self, event):
        self.key_notifier.add_key(event.key())

    def __update_position__(self, key):
        if key == Qt.Key_Left:
            self.player1_thread = Thread(target=self.player.movePlayerLeft, args=[self.player_label, ])
            self.player1_thread.start()
        elif key == Qt.Key_Right:
            self.player1_thread = Thread(target=self.player.movePlayerRight, args=[self.player_label, ])
            self.player1_thread.start()
        elif key == Qt.Key_Up:
            self.player1_thread = Thread(target=self.player.movePlayerUp, args=[self.player_label, ])
            self.player1_thread.start()
        elif key == Qt.Key_Down:
            self.player1_thread = Thread(target=self.player.movePlayerDown, args=[self.player_label, ])
            self.player1_thread.start()

        if key == Qt.Key_A:
            self.player2_thread = Thread(target=self.player2.movePlayerLeft, args=[self.player2_label, ])
            self.player2_thread.start()
        elif key == Qt.Key_D:
            self.player2_thread = Thread(target=self.player2.movePlayerRight, args=[self.player2_label, ])
            self.player2_thread.start()
        elif key == Qt.Key_W:
            self.player2_thread = Thread(target=self.player2.movePlayerUp, args=[self.player2_label, ])
            self.player2_thread.start()
        elif key == Qt.Key_S:
            self.player2_thread = Thread(target=self.player2.movePlayerDown, args=[self.player2_label, ])
            self.player2_thread.start()

    def closeEvent(self, event):
        self.key_notifier.die()

    """Funkcija ce se pozvati kada jedan player izgubi sve zivote
       Vraca tuple (winner_id, winner_name)
    """
    def calculate_winner(self):
        if int(self.label_for_player_score.text()) < int(self.label_for_player2_score.text()):
            return (self.player2.player_id, self.player2_name_label.text().capitalize())
        elif int(self.label_for_player_score.text()) > int(self.label_for_player2_score.text()):
            return (self.player.player_id, self.player1_name_label.text().capitalize())
        else:
            return ()


    def reset_player_smart(self):
        if self.player.player_eated == True and self.player2 == None:
            self.player.in_reset = True
            self.reset_player(self.player)
            self.player.player_eated = False
            self.player.in_reset = False
            return
        elif self.player2 != None and self.player2.player_eated == True:
            self.player2.in_reset = True
            self.player.in_reset = True
            self.reset_player(self.player2)
            self.player2.player_eated = False
            self.player2.in_reset = False
            self.player.in_reset = False
            return
        elif self.player.player_eated == True and self.player2 != None and self.player2.player_eated == False:
            self.player2.in_reset = True
            self.player.in_reset = True
            self.reset_player(self.player)
            self.player.player_eated = False
            self.player2.in_reset = False
            self.player.in_reset = False
            return

    def reset_player(self, player):
        next_players = []
        if self.play_mode == 1: # Singleplayer
            if player.player_lifes == -1:
                player.label.setHidden(True)
                player.label.move(900,900)
                self.image_label_for_winner_or_next_player.setPixmap(QPixmap('images/WinLabel.png'))
                self.image_label_for_winner_or_next_player.setHidden(False)
                self.winner_label.move(200, 50)
                self.winner_label.setText('   GAME OVER :(\n Your scroe: '+ str(player.current_score))
                sleep(4)
                self.close()
            else:
                player.label.setHidden(True)
                player.dead_label.setPixmap(QPixmap('images/Grave.png'))
                player.dead_label.setHidden(False)
                player.dead_label.move(player.label.x(), player.label.y())
                self.do_initial_countdown()
                player.dead_label.setHidden(True)
                player.label.setHidden(False)
                player.label.move(player.start_position[0], player.start_position[1])
                player.label.setPixmap(QPixmap('images/PacManUpEat' + str(player.player_id) + '.png'))

        elif self.play_mode == 2: # Multiplayer
            if self.player.player_lifes == -1 and self.player2.player_lifes > -1:
                self.player.label.setHidden(True)
                self.player.label.move(900,900)
                self.player.player_lifes = -2
                #self.player.in_reset = True
                self.do_initial_countdown()
            elif self.player.player_lifes > -1 and self.player2.player_lifes == -1:
                self.player2.label.setHidden(True)
                self.player2.label.move(900,900)
                self.player2.player_lifes = -2
                #self.player2.in_reset = True
                self.do_initial_countdown()
            elif self.player.player_lifes == -2 and self.player2.player_lifes == -1 or self.player.player_lifes == -1 and self.player2.player_lifes == -2:
                winner_id, winner_name = self.calculate_winner()
                self.image_label_for_winner_or_next_player.setPixmap(QPixmap('images/ChampionLabel.png'))
                self.image_label_for_winner_or_next_player.setHidden(False)
                self.winner_label.move(200, 50)
                if winner_id == 1:
                    winning_score = self.player.current_score
                else:
                    winning_score = self.player2.current_score
                self.winner_label.setText(f"{winner_name} je pobednik!\n Winning score: "+str (winning_score))
                sleep(4)
                self.close()
            elif player.player_lifes > -1:
                player.label.setHidden(True)
                player.dead_label.setPixmap(QPixmap('images/Grave.png'))
                player.dead_label.setHidden(False)
                player.dead_label.move(player.label.x(), player.label.y())
                self.do_initial_countdown()
                player.dead_label.setHidden(True)
                player.label.setHidden(False)
                player.label.move(player.start_position[0], player.start_position[1])
                player.label.setPixmap(QPixmap('images/PacManUpEat' + str(player.player_id) + '.png'))

        elif self.play_mode in (4, 8):
            if self.player.player_lifes == -1 and self.player2.player_lifes > -1:
                self.player.label.setHidden(True) #ovde mi bilo process.terminate()
                self.player.label.move(900, 900)
                self.player.player_lifes = -2
                self.do_initial_countdown()
            elif self.player.player_lifes > -1 and self.player2.player_lifes == -1:
                self.player2.label.setHidden(True)
                self.player2.label.move(900, 900)
                self.player2.player_lifes = -2
                self.do_initial_countdown()
            elif self.player.player_lifes == -2 and self.player2.player_lifes == -1 or self.player.player_lifes == -1 and self.player2.player_lifes == -2:
                next_players = self.calculate_next_players()
                winner_id, winner_name = self.calculate_winner()
                self.list_of_player_names.append((winner_id, winner_name))
                while len(self.list_of_player_names) != self.play_mode:
                    self.list_of_player_names.append(('', ''))
                self.tournament_window.round_done(winner_id, winner_name)
                if next_players[1][1] != '':
                    self.image_label_for_winner_or_next_player.setPixmap(QPixmap('images/WinLabel.png'))
                    self.image_label_for_winner_or_next_player.setHidden(False)
                    self.winner_label.setText(f"{winner_name} je pobednik!")
                    self.next_players_label.setText(f"Sledeci igraci: {next_players[0][1]} i {next_players[1][1]}")
                    self.restart_btn.setHidden(False)
                    while self.restart_btn_pushed == False:
                        #QCoreApplication.processEvents()
                        pass
                else:
                        self.image_label_for_winner_or_next_player.setPixmap(QPixmap('images/ChampionLabel.png'))
                        self.image_label_for_winner_or_next_player.setHidden(False)
                        self.winner_label.setText(f"{winner_name} je sampion!")
                        sleep(4)
                        self.close()

            elif player.player_lifes > -1:
                player.label.setHidden(True)
                player.dead_label.setPixmap(QPixmap('images/Grave.png'))
                player.dead_label.setHidden(False)
                player.dead_label.move(player.label.x(), player.label.y())
                self.do_initial_countdown()
                player.dead_label.setHidden(True)
                player.label.setHidden(False)
                player.label.move(player.start_position[0], player.start_position[1])
                player.label.setPixmap(QPixmap('images/PacManUpEat' + str(player.player_id) + '.png'))

    """Funkcija vraca sledeca 2 playera [(player1_id, player1_name), (player2_id, player2_name)]"""
    def calculate_next_players(self):
        player1_name = self.player1_name_label.text()
        player2_name = self.player2_name_label.text()

        self.list_of_player_names = [player for player in self.list_of_player_names if player[1].capitalize() != player1_name and player[1].capitalize() != player2_name and player[1].capitalize() != '']

        return self.list_of_player_names


    """Ovde ce na pritisak dugmeta Play da se pojave sledeca dvojica i da krene igra za njih"""
    @pyqtSlot()
    def on_end_game(self):
        new_game = MainWindow(self.list_of_player_names, self.tournament_window)
        self.close()
        new_game.show()

################################################################################################



########################### ENEMY FUNCTIONS ###################################################

    # iscrtavanje protivnika
    def draw_ghosts(self):
        self.blue_ghost_pixmap = QPixmap("images/Ghost4Down1.png")
        self.orange_ghost_pixmap = QPixmap("images/Ghost2Down1.png")
        self.red_ghost_pixmap = QPixmap("images/Ghost1Down1.png")
        self.yellow_ghost_pixmap = QPixmap("images/Ghost3Down1.png")

        self.blue_ghost.setPixmap(self.blue_ghost_pixmap)
        self.orange_ghost.setPixmap(self.orange_ghost_pixmap)
        self.red_ghost.setPixmap(self.red_ghost_pixmap)
        self.yellow_ghost.setPixmap(self.yellow_ghost_pixmap)

        self.blue_ghost.resize(40, 40)
        self.orange_ghost.resize(40, 40)
        self.red_ghost.resize(40, 40)
        self.yellow_ghost.resize(40, 40)

        self.blue_ghost.move(360, 360)
        self.red_ghost.move(360, 400)  # 720
        self.orange_ghost.move(440, 360)
        self.yellow_ghost.move(440, 400)

    def start_enemies(self):
        red_ghost_movement = Thread(target=self.change_mode_of_enemies)
        red_ghost_movement.daemon = True
        red_ghost_movement.start()

    def change_mode_of_enemies(self):
        self.do_initial_countdown()
        second_counter = 0
        self.mode = 0  # 0 - scatter, 1 - chase, 2 - frightened, 3 - eaten, 4 - reset
        enter_scatter = True
        enter_chase = False
        self.enter_frightened = False
        passed_10_seconds = False
        self.switch_if_needed(0)  # init u scatter
        while True:
            sleep(0.5)
            second_counter += 0.5
            if second_counter == 10:
                enter_scatter = False
                enter_chase = True
            elif second_counter == 0:
                passed_10_seconds = True
                self.deactivate_ghost_warning_skin()
            elif second_counter == 30.5:
                second_counter = 0
                enter_scatter = True
                enter_chase = False
            elif second_counter == -3:
                self.activate_ghost_warning_skin()

            if self.mode == 4:
                self.player.set_reset_mode_from_enemy(-1)
                if self.player2 != None:
                    self.player2.set_reset_mode_from_enemy(-1)
                second_counter = 0
                enter_scatter = True
                enter_chase = False
                self.enter_frightened = False
                passed_10_seconds = False
                self.reset_ghosts()
                self.reset_player_smart()
                self.mode = 0
                self.switch_mode_for_enemies()
                continue

            if self.player.return_reset_for_enemies() == 4:  # Reset
                self.mode = 4
                self.switch_if_needed(4)
                continue

            if self.player2 != None:
                if self.player2.return_reset_for_enemies() == 4:  # Reset
                    self.mode = 4
                    self.switch_if_needed(4)
                    continue

            if self.ghost1.check_if_player_activated_eat_ghost_power():
                self.enter_frightened = True

            else:
                self.enter_frightened = False


            if self.mode == 2 and self.ghost1.eated == True:
                self.ghost1.eated = False
                self.ghost1.mode = 3
                self.ghost1.switch_mode()

            if self.mode == 2 and self.ghost2.eated == True:
                self.ghost2.eated = False
                self.ghost2.mode = 3
                self.ghost2.switch_mode()

            if self.mode == 2 and self.ghost3.eated == True:
                self.ghost3.eated = False
                self.ghost3.mode = 3
                self.ghost3.switch_mode()

            if self.mode == 2 and self.ghost4.eated == True:
                self.ghost4.eated = False
                self.ghost4.mode = 3
                self.ghost4.switch_mode()

            if self.mode == 2 and (self.ghost1.mode == 0 or self.ghost1.mode == 1) and self.enter_frightened == True:
                self.ghost1.mode = 2
                self.ghost1.switch_mode()

            if self.mode == 2 and (self.ghost2.mode == 0 or self.ghost2.mode == 1) and self.enter_frightened == True:
                self.ghost2.mode = 2
                self.ghost2.switch_mode()

            if self.mode == 2 and (self.ghost3.mode == 0 or self.ghost3.mode == 1) and self.enter_frightened == True:
                self.ghost3.mode = 2
                self.ghost3.switch_mode()

            if self.mode == 2 and (self.ghost4.mode == 0 or self.ghost4.mode == 1) and self.enter_frightened == True:
                self.ghost4.mode = 2
                self.ghost4.switch_mode()

            if self.ghost1.mode == 3 and self.ghost1.reborned == True and self.enter_frightened == False:
                if enter_scatter == True:
                    self.ghost1.mode = 0
                elif enter_chase == True:
                    self.ghost1.mode = 1
                self.ghost1.switch_mode()

            if self.ghost2.mode == 3 and self.ghost2.reborned == True and self.enter_frightened == False:

                if enter_scatter == True:
                    self.ghost2.mode = 0
                elif enter_chase == True:
                    self.ghost2.mode = 1
                self.ghost2.switch_mode()

            if self.ghost3.mode == 3 and self.ghost3.reborned == True and self.enter_frightened == False:
                if enter_scatter == True:
                    self.ghost3.mode = 0
                elif enter_chase == True:
                    self.ghost3.mode = 1
                self.ghost3.switch_mode()

            if self.ghost4.mode == 3 and self.ghost4.reborned == True and self.enter_frightened == False:
                if enter_scatter == True:
                    self.ghost4.mode = 0
                elif enter_chase == True:
                    self.ghost4.mode = 1
                self.ghost4.switch_mode()

            if self.mode == 0 and enter_chase == True and self.enter_frightened == False:
                self.mode = 1
                self.switch_if_needed(1)
                continue

            elif self.mode == 0 and self.enter_frightened == True:
                self.mode = 2
                second_counter = -10
                passed_10_seconds = False
                self.switch_if_needed(2)
                continue

            elif self.mode == 1 and enter_scatter == True and self.enter_frightened == False:
                self.mode = 0
                self.switch_if_needed(0)
                continue

            elif self.mode == 1 and self.enter_frightened == True:
                self.mode = 2
                second_counter = -10
                passed_10_seconds = False
                self.switch_if_needed(2)
                continue

            elif self.mode == 2 and enter_scatter == True and self.enter_frightened == False and passed_10_seconds == True:
                self.mode = 0
                self.switch_if_needed(0)
                continue

            elif self.mode == 2 and enter_chase == True and self.enter_frightened == False and passed_10_seconds == True:
                self.mode = 1
                self.switch_if_needed(1)
                continue

            elif self.mode == 2 and self.enter_frightened == True:
                self.deactivate_ghost_warning_skin()
                second_counter = -10
                passed_10_seconds = False
                continue

    def switch_if_needed(self, to_mode: int):
        if self.ghost1.mode != to_mode and to_mode == 4:
            self.ghost1.mode = to_mode
            self.ghost1.switch_mode()
        elif self.ghost1.mode != to_mode and self.ghost1.mode != 3:
            self.ghost1.mode = to_mode
            self.ghost1.switch_mode()

        if self.ghost2.mode != to_mode and to_mode == 4:
            self.ghost2.mode = to_mode
            self.ghost2.switch_mode()
        elif self.ghost2.mode != to_mode and self.ghost2.mode != 3:
            self.ghost2.mode = to_mode
            self.ghost2.switch_mode()

        if self.ghost3.mode != to_mode and to_mode == 4:
            self.ghost3.mode = to_mode
            self.ghost3.switch_mode()
        elif self.ghost3.mode != to_mode and self.ghost3.mode != 3:
            self.ghost3.mode = to_mode
            self.ghost3.switch_mode()

        if self.ghost4.mode != to_mode and to_mode == 4:
            self.ghost4.mode = to_mode
            self.ghost4.switch_mode()
        elif self.ghost4.mode != to_mode and self.ghost4.mode != 3:
            self.ghost4.mode = to_mode
            self.ghost4.switch_mode()

    def switch_mode_for_enemies(self):
        self.ghost1.switch_mode()
        self.ghost2.switch_mode()
        self.ghost3.switch_mode()
        self.ghost4.switch_mode()

    def reset_ghosts(self):
        self.blue_ghost.move(self.ghost4.start_position[0], self.ghost4.start_position[1])
        self.orange_ghost.move(self.ghost2.start_position[0], self.ghost2.start_position[1])
        self.red_ghost.move(self.ghost1.start_position[0], self.ghost1.start_position[1])
        self.yellow_ghost.move(self.ghost3.start_position[0], self.ghost3.start_position[1])
        self.ghost1.reset_enemy()
        self.ghost2.reset_enemy()
        self.ghost3.reset_enemy()
        self.ghost4.reset_enemy()

    def activate_ghost_warning_skin(self):
        self.ghost1.activated_warning_skin = True
        self.ghost2.activated_warning_skin = True
        self.ghost3.activated_warning_skin = True
        self.ghost4.activated_warning_skin = True

    def deactivate_ghost_warning_skin(self):
        self.ghost1.activated_warning_skin = False
        self.ghost2.activated_warning_skin = False
        self.ghost3.activated_warning_skin = False
        self.ghost4.activated_warning_skin = False
        self.ghost1.next_warning_skin1 = False
        self.ghost2.next_warning_skin1 = False
        self.ghost3.next_warning_skin1 = False
        self.ghost4.next_warning_skin1 = False
        self.ghost1.next_warning_skin2 = False
        self.ghost2.next_warning_skin2 = False
        self.ghost3.next_warning_skin2 = False
        self.ghost4.next_warning_skin2 = False

################################################################################################



########################### POWERS FUNCTIONS ###################################################

    def changeSpecialPowerLocation(self, showed_time, hidden_time):  # Funkcija prima showed_time koja nam zadaje za koliko ce sekundi da se pojavi special power, a hidden_time da posle koliko sekundi ce se sakriti
        showing_time = showed_time
        hidding_time = hidden_time
        first_time = True
        there_was_coin = False
        i = 1
        while True:
            if first_time:
                self.hideSpecialPower(hidding_time)
                self.map.board[self.niz_lokacija_special_power[0][1]][self.niz_lokacija_special_power[0][0]] = 2
                first_time = False
            else:
                if self.map.is_coin(self.niz_lokacija_special_power[i][0] * 40, self.niz_lokacija_special_power[i][1] * 40):
                    there_was_coin = True
                else:
                    there_was_coin = False

                sleep(showing_time)
                if self.label_super_power.isHidden():
                    self.label_super_power.setHidden(False)
                    self.map.board[self.niz_lokacija_special_power[i][1]][self.niz_lokacija_special_power[i][0]] = 4
                    if self.player_label.x() == self.niz_lokacija_special_power[i][0] * 40 and self.player_label.y() == self.niz_lokacija_special_power[i][1] * 40 :
                        self.label_super_power.setHidden(True)

                self.label_super_power.move(self.niz_lokacija_special_power[i][0] * 40, self.niz_lokacija_special_power[i][1] * 40)

                self.hideSpecialPower(hidding_time)
                if there_was_coin:
                    self.map.board[self.niz_lokacija_special_power[i][1]][self.niz_lokacija_special_power[i][0]] = 2
                i += 1
                if i == 5:
                    i = 0

    def hideSpecialPower(self, hidding_time):
        sleep(hidding_time)
        self.label_super_power.setHidden(True)



################################################################################################

    """Center screen"""

    def center_window(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)


##################################################################################################

class Board(QFrame):
    board_width = 800
    board_height = 640

    def __init__(self, parent):
        super().__init__(parent)

        self.resize(self.board_width, self.board_height)
        # 0 => zid    1=> tunel  2=> Coin  3=> Eat_Ghost
        self.board = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 3, 2, 2, 0, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 0, 2, 2, 2, 0],
            [0, 2, 0, 2, 2, 2, 0, 0, 0, 2, 2, 2, 0, 0, 2, 2, 2, 0, 2, 0],
            [0, 2, 2, 2, 0, 2, 2, 2, 2, 2, 0, 2, 2, 0, 2, 0, 3, 2, 2, 0],
            [0, 0, 2, 0, 0, 2, 2, 0, 2, 3, 0, 2, 2, 2, 2, 2, 0, 2, 2, 0],
            [0, 2, 2, 2, 0, 0, 2, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 0, 2, 0],
            [0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 0, 2, 0, 0, 2, 0, 0, 2, 2, 0],
            [0, 2, 2, 3, 2, 2, 0, 2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0],
            [2, 2, 2, 0, 0, 2, 2, 2, 0, 0, 1, 0, 0, 2, 0, 0, 0, 2, 2, 2],
            [0, 0, 2, 0, 0, 2, 0, 2, 0, 1, 1, 1, 0, 2, 2, 0, 3, 0, 2, 0],
            [0, 2, 2, 3, 2, 2, 2, 2, 0, 1, 1, 1, 0, 0, 2, 0, 2, 2, 2, 0],
            [0, 2, 0, 2, 0, 0, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 2, 0],
            [0, 2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 0, 2, 0],
            [0, 2, 2, 2, 0, 2, 0, 0, 0, 3, 0, 2, 2, 0, 2, 2, 2, 2, 2, 0],
            [0, 1, 0, 2, 2, 2, 0, 0, 0, 2, 2, 2, 0, 0, 2, 2, 2, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ]

        self.special_power_locations = []
        self.populate_super_power_indices(self.board,
                                          3)  # vraca indekse svih elemenata cija je vrednost 4 iz matrice board

    def is_tunnel(self, x,
                  y):  # Vraca true ako je tunel, tj. omogucava kretanje PacMan-a. Ako je element matrice 0(zid) onda vraca false, tj. zabranjuje prolazak PacMan-a.
        if (x % 40 == 0 and y % 40 == 0):
            if self.board[y // 40][x // 40] == 1:
                return True
        else:
            return False

    def is_coin(self, x, y):
        if (x % 40 == 0 and y % 40 == 0):
            if self.board[y // 40][x // 40] == 2:
                winsound.PlaySound("images/pacman_chomp.wav", winsound.SND_ASYNC | winsound.SND_ALIAS)
                return True
        else:
            return False

    def is_eat_ghosts_power(self, x, y):
        if (x % 40 == 0 and y % 40 == 0):
            if self.board[y // 40][x // 40] == 3:
                winsound.PlaySound("images/pacman_eatfruit.wav", winsound.SND_ASYNC | winsound.SND_ALIAS)
                return True
            else:
                return False
        else:
            return False

    def is_deus_ex_machina_power(self, x, y):
        if (x % 40 == 0 and y % 40 == 0):
            if self.board[y // 40][x // 40] == 4:
                return True
            else:
                return False
        else:
            return False

    def zid(self, x, y):
        if (x % 40 == 0 and y % 40 == 0):
            if x == 800:
                self.reset_coins_if_needed()
                return True
            if x == -40:
                self.reset_coins_if_needed()
                return True
            if self.board[y // 40][x // 40] != 0:
                return True
        else:
            return False

    def is_wall(self, x, y):
        # if (x % 40 == 0 and y % 40 == 0):
        if x == 800:
            return False
        if x == -40:
            return False
        if self.board[y // 40][x // 40] == 0:
            return False
        return True

    def paintEvent(self, event):
        painter = QPainter(self)

        for i in range(20):
            for j in range(16):
                if self.board[j][i] == 0:
                    # draw wall
                    self.draw_map(i * 40, j * 40, painter, Qt.darkBlue)
                elif self.board[j][i] == 2:
                    self.draw_coins(i, j, painter)
                elif self.board[j][i] == 3:
                    self.draw_eat_ghost_power(i, j, painter)
                elif self.board[j][i] == 4:
                    self.draw_map(i * 40, j * 40, painter, Qt.black)  # Za pocetak da crta tunel
                else:
                    self.draw_map(i * 40, j * 40, painter, Qt.black)  # tunel

    def draw_map(self, x, y, painter, color):
        painter.fillRect(x, y, 40, 40, color)

    def draw_coins(self, i, j, painter):
        painter.drawPixmap(i * 40, j * 40, QPixmap('images/Coin.png'))

    def draw_black_background(self, x, y):  # Kad PacMan "pojede" coin, coin se zamenjuje crnom slikom
        self.board[y // 40][x // 40] = 1

    def draw_eat_ghost_power(self, i, j, painter):
        painter.drawPixmap(i * 40, j * 40, QPixmap('images/EatGhostsPower1.png'))

    def populate_super_power_indices(self, board, value):
        for i in range(20):
            for j in range(16):
                if board[j][i] == value:
                    self.special_power_locations.append((i * 40, j * 40))

    def reset_coins_if_needed(self):
        for i in range(20):
            for j in range(16):
                if self.board[j][i] == 2:
                    return

        for i in range(20):
            for j in range(16):
                if self.board[j][i] == 1:
                    self.board[j][i] = 2

        self.board[8][10] = 1
        self.board[9][9] = 1
        self.board[9][10] = 1
        self.board[9][11] = 1
        self.board[10][9] = 1
        self.board[10][10] = 1
        self.board[10][11] = 1
        self.board[14][1] = 1
        self.board[14][18] = 1

        self.update()