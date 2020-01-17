
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
import player
from time import sleep, time
from math import sqrt, floor, atan2, degrees
import math
from operator import itemgetter
from random import randint
from threading import Thread
import multiprocessing


class Enemy(QLabel):

    def __init__(self, label, map, player, player2, scatter_target, ghost_id, red_ghost_label, start_position):
        super().__init__()

        self.label = label
        self.map = map
        self.player = player
        self.player2 = player2
        self.red_ghost = red_ghost_label
        self.scatter_target = scatter_target # prosledjen Tuple, potrebno je ih pomnoziti sa 40 da bi se dobila pozicija na mapi
        self.ghost_id = ghost_id # ghost_id odredjuje koji kretajuci pattern prati
        self.zero_point = (400, 320)
        self.target_home = (400, 400)
        self.eaten = False
        self.activated_frightened = False
        self.reborned = False # da li se vratio ghost na pocetno mesto kad ga je pacman pojeo
        self.zero_point_passed = False # polje ispred kuce, odatle znaju da se krecu u odgovarajuce pravce, sve dok ga ne predju a nalaze se u kucici, ne mogu da izadju pomocu osnovnog algoritma
        self.activated_warning_skin = False
        self.next_warning_skin1 = False
        self.next_warning_skin2 = False
        self.mode = 5  # 0 - scatter mode
                       # 1 - chase mode
                       # 2 - frightened mode
                       # 3 - eaten
                       # 4 - reset
        self.previous_direction = 2 # 0 - dole
                                    # 1 - levo
                                    # 2 - gore
                                    # 3 - desno
        self.previous_eated_num_of_eat_ghost_powers_by_player = 0
        self.start_position = start_position
        self.currentProcess = None
        self.eated = False
        self.stop_movement = False
        self.ghost_speed = 0.07


    def move_chase(self): # ide za pacmanom
        self.stop_movement = False
        decreased_player_life = False
        if self.zero_point_passed == False:
            while self.zero_point_passed == False and not self.stop_movement and self.mode == 1:
                self.move_one_to_target((self.zero_point[0], self.zero_point[1]))
                self.check_if_zero_point_passed()
        while self.mode == 1 and not self.stop_movement: # while chase mode
            self.move_one_to_target(self.calculate_chase_position(self.player.return_current_player_position(), self.ghost_id))
            if self.player.ghost_speed_up == True:
                self.ghost_speed = 0.06
            else:
                self.ghost_speed = 0.07
            if self.check_if_touch_happened():
                if not decreased_player_life:
                    if self.player.player_eated == True:  # uhvatio je prvog igraca
                        self.player.decrease_player_lifes()
                    if self.player2 != None:  # uhvatio je drugog igraca
                        if self.player2.player_eated == True:
                            self.player2.decrease_player_lifes()
                    decreased_player_life = True

    def move_scatter(self): # ide u svoj ugao
        self.stop_movement = False
        decreased_player_life = False
        if self.zero_point_passed == False:
            while self.zero_point_passed == False and not self.stop_movement and self.mode == 0:
                self.move_one_to_target((self.zero_point[0], self.zero_point[1]))
                self.check_if_zero_point_passed()
        while self.mode == 0 and not self.stop_movement:
            if self.player.ghost_speed_up == True:
                self.ghost_speed = 0.06
            else:
                self.ghost_speed = 0.07
            if self.check_if_touch_happened():
                if not decreased_player_life:
                    if self.player.player_eated == True:  # uhvatio je prvog igraca
                        self.player.decrease_player_lifes()
                    elif self.player2 != None:  # uhvatio je drugog igraca
                        if self.player2.player_eated == True:
                            self.player2.decrease_player_lifes()
                    decreased_player_life = True
            else:
                self.move_one_to_target((self.scatter_target[0], self.scatter_target[1]))


    def move_frightened(self): # okrene se za 180 stepeni i random krece da se pomera
        self.ghost_speed = 0.09
        self.stop_movement = False
        increased = False
        if self.zero_point_passed == False:
            while self.zero_point_passed == False and not self.stop_movement and self.mode == 2:
                self.move_one_to_target((self.zero_point[0], self.zero_point[1]))
                self.check_if_zero_point_passed()
        while self.mode == 2 and not self.stop_movement:
            if self.check_if_touch_happened():
                if increased == False:
                    if self.player.player_eated == True:  # uhvatio je prvog igraca
                        self.player.increase_points(200)
                        #self.player.player_eated == False
                    if self.player2 != None:  # uhvatio je drugog igraca
                        if self.player2.player_eated == True:
                            self.player2.increase_points(200)
                            #self.player2.player_eated == False
                    self.eaten = True
                    self.eated = True
                    self.reborned = False
                    increased = True
            else:
                self.move_random_one()

    def move_eaten(self): # vraca se na pocetnu poziciju, na 400 400
        self.ghost_speed = 0.05
        while not self.reborned and self.mode != 4:
            if self.check_if_ghost_returned_to_home():
                self.reborned = True
                self.eaten = False
                self.eated = False
                self.zero_point_passed = False
                self.ghost_speed = 0.07
                #self.mode = 0
                #print('prev was in SCATTER pa mora u SCATTER')
                #self.switch_mode()
            else:
                self.move_one_to_target(self.start_position)

    def check_if_zero_point_passed(self): # zero point: X> 400 Y > 280. Logika: Ako zero point nije predjen, protivnik treba prvo do njega da dodje.
        if self.label.x() == 400 and self.label.y() == 280:
            if self.zero_point_passed == True:
                self.zero_point_passed = False
            elif self.zero_point_passed == False:
                self.zero_point_passed = True

    def calculate_chase_position(self, player, ghost_id): # Funckija vraca Tuple, prva vrednost je X koordinata, druga Y koordinata koju juri ghost
        if ghost_id == 1: # RED ghost, vija tacno pacman-ovu poziciju
            return (player[0], player[1])
        elif ghost_id == 2: # ORANGE ghost, juri pozicije: 2 pozicije ulevo, 2 pozicije udesno, 2 pozicije ka dole, i 2 pozicije levo i gore ako se krece ka gore.
            if self.previous_direction == 0: # Ako je pre isao ka dole, onda juri 2 pozicije ka dole od pacman-a
                return (player[0], player[1] + 80)
            elif self.previous_direction == 1: # Ako je pre isao ka levo, onda juri 2 pozicije ulevo u odnosu na pravac
                return (player[0]-80, player[1])
            elif self.previous_direction == 2: # Ako je pre isao ka gore, onda je target 2 pozicije ulevo i 2 ka gore
                return (player[0]-80, player[1]-80)
            elif self.previous_direction == 3: # Ako je pre osao ka desno, vraca 2 pozicije udesno
                return (player[0]+80, player[1])
        elif ghost_id == 3: # YELLOW ghost
             return self.calculate_for_yellow_ghost(player)
        elif ghost_id == 4: # BLUE ghost, juri pozicije kao i ORANGE ghost, s tim, da u obrnutom pravcu, tj 180 stepeni drugi smer u odnosu na poziciju RED ghost-a
            if self.previous_direction == 0: # Ako je pre isao ka dole, onda juri 2 pozicije ka dole od pacman-a
                return self.calculate_for_blue_ghost(self.red_ghost, player[0], player[1] + 80)
            elif self.previous_direction == 1: # Ako je pre isao ka levo, onda juri 2 pozicije ulevo u odnosu na pravac
                return self.calculate_for_blue_ghost(self.red_ghost, player[0] - 80, player[1])
            elif self.previous_direction == 2: # Ako je pre isao ka gore, onda je target 2 pozicije ulevo i 2 ka gore
                return self.calculate_for_blue_ghost(self.red_ghost, player[0] - 80, player[1] - 80)
            elif self.previous_direction == 3: # Ako je pre osao ka desno, vraca 2 pozicije udesno
                return self.calculate_for_blue_ghost(self.red_ghost, player[0] + 80, player[1])

    def calculate_for_blue_ghost(self, red_ghost_position, playerX, playerY): # Vraca X i Y za blue
        distance = sqrt((abs(red_ghost_position.x() - (playerX)) ** 2) + (abs(red_ghost_position.y() - (playerY)) ** 2))
        degrees180 = (math.degrees(atan2(red_ghost_position.y() - playerY, red_ghost_position.x() - playerX)) + 180) % 360
        return (playerX + distance*math.cos(degrees180),playerY + distance*math.sin(degrees180))

    def calculate_for_yellow_ghost(self, player):
        distance = sqrt((abs(player[0] - (self.label.x())) ** 2) + (abs(player[1] - (self.label.y())) ** 2))
        if distance < 80: # Scatter mode
            return (self.scatter_target[0], self.scatter_target[1])
        elif distance > 80 or distance == 80: # Direct chase
            return (player[0], player[1])

    def move_one_to_target(self, target): # Prima False uslov, metoda uslov_za_izlazak treba da postavi globalnu promenljivu i da vrati vrednost tu vrednost uslov promenljivi, kako bi se zavrsila ova metoda
        pravac1 = (1,1000)  # Maximum odstojanje je 466, pa ako se za neki pravac ne moze odrediti vrednost(napr. zid), nek ne utice na novi pravac
        pravac2 = (2, 1000)
        pravac3 = (3, 1000)
        #print('x>>',target[0],'  y>>',target[1])
        if self.previous_direction == 0:  # pre isao ka dole
            if self.map.is_wall(self.label.x() - 40, self.label.y()):  # LEVO
                pravac1 = (1, sqrt((abs(target[0] - (self.label.x() - 40)) ** 2) + (abs(target[1] - self.label.y()) ** 2)))
            if self.map.is_wall(self.label.x() + 40, self.label.y()):  # DESNO
                pravac2 = (3, sqrt((abs(target[0] - (self.label.x() + 40)) ** 2) + (abs(target[1] - self.label.y()) ** 2)))
            if self.map.is_wall(self.label.x(), self.label.y() + 40):  # NASTAVI DOLE
                pravac3 = (0, sqrt((abs(target[0] - (self.label.x())) ** 2) + (abs(target[1] - (self.label.y() + 40)) ** 2)))
            pravci = [pravac1, pravac3, pravac2]
            if pravac1[1] != 1000 or pravac2[1] != 1000 or pravac3[1] != 1000:
                self.previous_direction = min(pravci, key=itemgetter(1))[0]
            else:
                self.previous_direction = 2
            self.move_to_direction(self.previous_direction)
            return
        elif self.previous_direction == 1:  # pre isao ka LEVO
            if self.map.is_wall(self.label.x() - 40, self.label.y()):  # NASTAVI LEVO
                pravac1 = (1, sqrt((abs(target[0] - (self.label.x() - 40)) ** 2) + (abs(target[1] - self.label.y()) ** 2)))
            if self.map.is_wall(self.label.x(), self.label.y() - 40):  # GORE
                pravac2 = (2, sqrt((abs(target[0] - (self.label.x())) ** 2) + (abs(target[1] - (self.label.y() - 40)) ** 2)))
            if self.map.is_wall(self.label.x(), self.label.y() + 40):  # DOLE
                pravac3 = (0, sqrt((abs(target[0] - (self.label.x())) ** 2) + (abs(target[1] - (self.label.y() + 40)) ** 2)))
            pravci = [pravac2, pravac1, pravac3]
            if pravac1[1] != 1000 or pravac2[1] != 1000 or pravac3[1] != 1000:
                self.previous_direction = min(pravci, key=itemgetter(1))[0]
            else:
                self.previous_direction = 3
            self.move_to_direction(self.previous_direction)
            return
        elif self.previous_direction == 2:  # pre isao ka GORE
            if self.map.is_wall(self.label.x() - 40, self.label.y()):  # LEVO
                pravac1 = (1, sqrt((abs(target[0] - (self.label.x() - 40)) ** 2) + (abs(target[1] - self.label.y()) ** 2)))
            if self.map.is_wall(self.label.x() + 40, self.label.y()):  # DESNO
                pravac2 = (3, sqrt((abs(target[0] - (self.label.x() + 40)) ** 2) + (abs(target[1] - self.label.y()) ** 2)))
            if self.map.is_wall(self.label.x(), self.label.y() - 40):  # NASTAVI GORE
                pravac3 = (2, sqrt((abs(target[0] - (self.label.x())) ** 2) + (abs(target[1] - (self.label.y() - 40)) ** 2)))
            pravci = [pravac3, pravac1, pravac2]
            if pravac1[1] != 1000 or pravac2[1] != 1000 or pravac3[1] != 1000:
                self.previous_direction = min(pravci, key=itemgetter(1))[0]
            else:
                self.previous_direction = 0
            self.move_to_direction(self.previous_direction)
            return
        elif self.previous_direction == 3:  # pre isao ka DESNO
            if self.map.is_wall(self.label.x(), self.label.y() - 40):  # GORE
                pravac1 = (2, sqrt((abs(target[0] - (self.label.x())) ** 2) + (abs(target[1] - (self.label.y() - 40)) ** 2)))
            if self.map.is_wall(self.label.x() + 40, self.label.y()):  # DESNO
                pravac2 = (3, sqrt((abs(target[0] - (self.label.x() + 40)) ** 2) + (abs(target[1] - self.label.y()) ** 2)))
            if self.map.is_wall(self.label.x(), self.label.y() + 40):  # NASTAVI DOLE
                pravac3 = (0, sqrt((abs(target[0] - (self.label.x())) ** 2) + (abs(target[1] - (self.label.y() + 40)) ** 2)))
            pravci = [pravac1, pravac3, pravac2]
            if pravac1[1] != 1000 or pravac2[1] != 1000 or pravac3[1] != 1000:
                self.previous_direction = min(pravci, key=itemgetter(1))[0]
            else:
                self.previous_direction = 1
            self.move_to_direction(self.previous_direction)
            return

    def check_if_ghost_returned_to_home(self): # Ako se vratio na pocetnu poziciju, rebornuje se
        if self.label.x() == self.start_position[0] and self.label.y() == self.start_position[1]:
            return True

    def move_one_180(self):
        if self.previous_direction == 0:  # DOLE
            self.move_to_direction(2)
        elif self.previous_direction == 1:  # LEVO
            self.move_to_direction(3)
        elif self.previous_direction == 2:  # GORE
            self.move_to_direction(0)
        elif self.previous_direction == 3:  # DESNO
            self.move_to_direction(1)

    def move_random_one(self):
        direction = randint(0,3)
        if direction == 0:  # DOLE
            if self.map.is_wall(self.label.x(), self.label.y() + 40):
                self.move_to_direction(direction)
        elif direction == 1:  # LEVO
            if self.map.is_wall(self.label.x() - 40, self.label.y()):
                self.move_to_direction(direction)
        elif direction == 2:  # GORE
            if self.map.is_wall(self.label.x(), self.label.y() - 40):
                self.move_to_direction(direction)
        elif direction == 3:  # DESNO
            if self.map.is_wall(self.label.x() + 40, self.label.y()):
                self.move_to_direction(direction)

    def move_to_direction(self, direction):
        for i in range(2):
            if direction == 0: # DOLE
                self.change_look_of_ghost(1, 'Down')
                self.label.move(self.label.x(), self.label.y() + 20)
                #QGuiApplication.processEvents()
                sleep(self.ghost_speed)
                self.change_look_of_ghost(2, 'Down')
                #QGuiApplication.processEvents()
                sleep(self.ghost_speed)
            elif direction == 1: # LEVO
                self.change_look_of_ghost(1, 'Left')
                self.label.move(self.label.x() - 20, self.label.y())
                # QGuiApplication.processEvents()
                sleep(self.ghost_speed)
                self.change_look_of_ghost(2, 'Left')
                # QGuiApplication.processEvents()
                sleep(self.ghost_speed)
            elif direction == 2: # GORE
                self.change_look_of_ghost(1, 'Up')
                self.label.move(self.label.x(), self.label.y() - 20)
                # QGuiApplication.processEvents()
                sleep(self.ghost_speed)
                self.change_look_of_ghost(2, 'Up')
                # QGuiApplication.processEvents()
                sleep(self.ghost_speed)
            elif direction == 3: # DESNO
                self.change_look_of_ghost(1, 'Right')
                self.label.move(self.label.x() + 20, self.label.y())
                # QGuiApplication.processEvents()
                sleep(self.ghost_speed)
                self.change_look_of_ghost(2, 'Right')
                # QGuiApplication.processEvents()
                sleep(self.ghost_speed)

    def change_look_of_ghost(self, picture_num, direction): # eye_direction -> Left, Right, Down, Up
        if picture_num == 1:
            if self.activated_frightened or self.mode == 2: # Moze se pojesti, tj uzima plavi skin
                #self.ghost_speed = 0.10
                if self.activated_warning_skin == True:
                    if self.next_warning_skin1 == False:
                        self.label.setPixmap(QPixmap('images/GhostDeadWhite1.png'))
                        self.next_warning_skin1 = True
                    else:
                        self.label.setPixmap(QPixmap("images/GhostDead1.png"))
                        self.next_warning_skin1 = False
                else:
                    self.label.setPixmap(QPixmap("images/GhostDead1.png"))
            elif self.eaten:
                self.label.setPixmap(QPixmap("images/Eyes"+direction+".png"))
            else:
                #self.ghost_speed = 0.06
                self.label.setPixmap(QPixmap("images/Ghost"+str(self.ghost_id)+str(direction)+"1.png"))
        elif picture_num == 2:
            if self.activated_frightened or self.mode == 2: # Moze se pojesti, tj uzima plavi skin
                #self.ghost_speed = 0.10
                if self.activated_warning_skin == True:
                    if self.next_warning_skin2 == False:
                        self.label.setPixmap(QPixmap('images/GhostDeadWhite2.png'))
                        self.next_warning_skin2 = True
                    else:
                        self.label.setPixmap(QPixmap("images/GhostDead2.png"))
                        self.next_warning_skin2 = False
                else:
                    self.label.setPixmap(QPixmap("images/GhostDead2.png"))
            elif self.eaten:
                self.label.setPixmap(QPixmap("images/Eyes"+direction+".png"))
            else:
                #self.ghost_speed = 0.06
                self.label.setPixmap(QPixmap("images/Ghost"+str(self.ghost_id)+str(direction)+"2.png"))

    def switch_mode(self):
        self.stop_movement = True
        if self.mode == 0:
             #multiprocessing.Process(target=self.move_scatter, args=[]).start()
            self.currentProcess = Thread(target=self.move_scatter)
            self.currentProcess.daemon = True
            self.currentProcess.start()
        elif self.mode == 1:
            self.currentProcess = Thread(target=self.move_chase)
            self.currentProcess.daemon = True
            self.currentProcess.start()
        elif self.mode == 2:
            self.currentProcess = Thread(target=self.move_frightened)
            self.currentProcess.daemon = True
            self.currentProcess.start()
        elif self.mode == 3:
            self.currentProcess = Thread(target=self.move_eaten)
            self.currentProcess.daemon = True
            self.currentProcess.start()
        elif self.mode == 4:
            self.stop_movement = True

    def check_if_player_activated_eat_ghost_power(self):
        current_eated = self.player.return_num_of_eated_ghost_powers_by_player()
        if self.player2 != None:
            current_eated += self.player2.return_num_of_eated_ghost_powers_by_player()
        if self.previous_eated_num_of_eat_ghost_powers_by_player < current_eated:
            self.previous_eated_num_of_eat_ghost_powers_by_player = current_eated
            return True
        else:
            return False

    def check_if_touch_happened(self):
        position = self.player.return_current_player_position()
        if self.player2 != None:
            position2 = self.player2.return_current_player_position()
        if self.previous_direction == 0:  # Dole
            if self.label.x() == position[0] and abs((self.label.y() + 40) - position[1]) < 41:
                # print('DOLE NASO TE ACOOOO AUUA')
                self.player.player_eated = True
                return True
            if self.player2 != None:
                if self.label.x() == position2[0] and abs((self.label.y() + 40) - position2[1]) < 41:
                    self.player2.player_eated = True
                    return True
        elif self.previous_direction == 1:  # LEVO
            if abs((self.label.x() - 40) - position[0]) < 41 and self.label.y() == position[1]:
                # print('LEVO NASO TE ACOOOO AUUA')
                self.player.player_eated = True
                return True
            if self.player2 != None:
                if abs((self.label.x() - 40) - position2[0]) < 41 and self.label.y() == position2[1]:
                    self.player2.player_eated = True
                    return True
        elif self.previous_direction == 2:  # GORE
            if self.label.x() == position[0] and abs((self.label.y() - 40) - position[1]) < 41:
                self.player.player_eated = True
                return True
            if self.player2 != None:
                if self.label.x() == position2[0] and abs((self.label.y() - 40) - position2[1]) < 41:
                    self.player2.player_eated = True
                    return True
        elif self.previous_direction == 3:  # DESNO
            if abs((self.label.x() + 40) - position[0]) < 41 and self.label.y() == position[1]:
                # print('DESNO NASO TE ACOOOO AUUA')
                self.player.player_eated = True
                return True
            if self.player2 != None:
                if abs((self.label.x() + 40) - position2[0]) < 41 and self.label.y() == position2[1]:
                    self.player2.player_eated = True
                    return True

    def reset_enemy(self):
        self.eaten = False  # da li ga je player pojeo
        self.activated_frightened = False
        self.reborned = False  # da li se vratio ghost na pocetno mesto kad ga je pacman pojeo
        self.zero_point_passed = False  # polje ispred kuce, odatle znaju da se krecu u odgovarajuce pravce, sve dok ga ne predju a nalaze se u kucici, ne mogu da izadju pomocu osnovnog algoritma
        self.activated_warning_skin = False
        self.next_warning_skin1 = False
        self.next_warning_skin2 = False
        self.mode = 0  # 0 - scatter mode
        self.eated = False
        self.stop_movement = False
        self.label.setPixmap(QPixmap("images/Ghost" + str(self.ghost_id)+"Down1.png"))
