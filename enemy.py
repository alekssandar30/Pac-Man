#kod za protivnike

# kod za protivnike
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
import player
from time import sleep
from math import sqrt, floor, atan2, degrees
import math
from operator import itemgetter


class Enemy(QLabel):
    def __init__(self, label, map, player, scatter_target, ghost_id, red_ghost_label):
        super().__init__()

        self.label = label
        self.map = map
        self.player = player
        self.red_ghost = red_ghost_label
        self.scatter_target = scatter_target # prosledjen Tuple, potrebno je ih pomnoziti sa 40 da bi se dobila pozicija na mapi
        self.ghost_id = ghost_id # ghost_id odredjuje koji kretajuci pattern prati
        self.eaten = False # da li ga je player pojeo
        self.activated_frightened = False
        self.reborned = False # da li se vratio ghost na pocetno mesto kad ga je pacman pojeo
        self.target_home = (400,400)
        self.mode = 1 # 0 - scatter mode
                      # 1 - chase mode
                      # 2 - frightened mode
                      # 3 - eaten

        self.change_mode_pattern = [(1, 7, 20, 7, 20, 5, 20, 5, 20), (2, 7, 20, 7, 20, 5, 17, 5, 25), (3, 7, 22, 7, 22, 5, 22, 5, 30)]
        # (1, 7, 20, 7, 20, 5, 20, 5, 20) => 1 - level, 7 sec scatter, 20 sec chase itd (scatter, chase) par

        #self.enemies = [self.blue_enemy, self.orange_enemy, self.red_enemy, self.rose_enemy, self.yellow_enemy]

        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.previous_direction = 2 # 0 - dole
                                    # 1 - levo
                                    # 2 - gore
                                    # 3 - desno

    def move_chase(self): # ide za pacmanom
        while self.mode == 1: # while chase mode
            self.move_one_to_target(self.calculate_chase_position(self.player.return_current_player_position(), self.ghost_id))
            #self.check_if_pacman_catched()


    def move_scatter(self): # ide u svoj ugao
        pass

    def move_frightened(self): # okrene se za 180 stepeni i random krece da se pomera
        pass

    def move_eaten(self): # vraca se na pocetnu poziciju, na 400 400
        while not self.reborned:
            self.move_one_to_target(self.target_home)
            #self.check_if_ghost_returned_to_home()

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
        #print('Player x>>',player[0],'  Player y>>',player[1])
        #print('Label x>>', self.label.x(), ' Label y>>', self.label.y())
        #print('Y - y>> ',player[1] -  self.label.y())
        distance = sqrt((abs(player[0] - (self.label.x())) ** 2) + (abs(player[1] - (self.label.y())) ** 2))
        if distance < 80: # Scatter mode
            return (self.scatter_target[0] * 40, self.scatter_target[1] * 40)
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
        if self.label.x() == self.target_home[0] and self.label.y() == self.target_home[1]:
            self.reborned = True

    def check_if_pacman_catched(self):
        pacman_position = self.player.return_current_player_position()
        if self.label.x() == pacman_position[0] and self.label.y() == pacman_position[1]:
            self.mode = 0 # treba da umanji pacmanov broj zivota i da ga resetuje na poziciju
            print('UHVATIO PACMANA')


    def move_to_direction(self, direction):
        for i in range(2):
            if direction == 0: # DOLE
                self.change_look_of_ghost(1, 'Down')
                self.label.move(self.label.x(), self.label.y() + 20)
                #QGuiApplication.processEvents()
                sleep(0.06)
                self.change_look_of_ghost(2, 'Down')
                #QGuiApplication.processEvents()
                sleep(0.06)
            elif direction == 1: # LEVO
                self.change_look_of_ghost(1, 'Left')
                self.label.move(self.label.x() - 20, self.label.y())
                # QGuiApplication.processEvents()
                sleep(0.06)
                self.change_look_of_ghost(2, 'Left')
                # QGuiApplication.processEvents()
                sleep(0.06)
            elif direction == 2: # GORE
                self.change_look_of_ghost(1, 'Up')
                self.label.move(self.label.x(), self.label.y() - 20)
                # QGuiApplication.processEvents()
                sleep(0.06)
                self.change_look_of_ghost(2, 'Up')
                # QGuiApplication.processEvents()
                sleep(0.06)
            elif direction == 3: # DESNO
                self.change_look_of_ghost(1, 'Right')
                self.label.move(self.label.x() + 20, self.label.y())
                # QGuiApplication.processEvents()
                sleep(0.06)
                self.change_look_of_ghost(2, 'Right')
                # QGuiApplication.processEvents()
                sleep(0.06)

    def change_look_of_ghost(self, picture_num, direction): # eye_direction -> Left, Right, Down, Up
        if picture_num == 1:
            if self.activated_frightened: # Moze se pojesti, tj uzima plavi skin
                self.label.setPixmap(QPixmap("images/GhostDead1.png"))
            elif self.eaten:
                self.label.setPixmap(QPixmap("images/Eyes"+direction+".png"))
            else:
                self.label.setPixmap(QPixmap("images/Ghost"+str(self.ghost_id)+str(direction)+"1.png"))
        elif picture_num == 2:
            if self.activated_frightened: # Moze se pojesti, tj uzima plavi skin
                self.label.setPixmap(QPixmap("images/GhostDead2.png"))
            elif self.eaten:
                self.label.setPixmap(QPixmap("images/Eyes"+direction+".png"))
            else:
                self.label.setPixmap(QPixmap("images/Ghost"+str(self.ghost_id)+str(direction)+"2.png"))

    def change_mode(self):
        second_counter = 0
        while True:
            sleep(0.5)
            second_counter += 0.5
            if self.mode == 0 and self.eaten == False and second_counter == 7:
                self.mode = 1
            elif self.mode == 1 and self.eaten == False and second_counter == 20:
                self.mode = 0
                second_counter = 0
            elif self.eaten:
                self.mode = 3
                self.move_eaten()
                self.eaten = False
            elif self.activated_frightened:
                self.mode = 2

    # move
    # imacu jednu metodu move koja ce "pametno" da poziva metode za kretanje
    # iz playera...

    def eated_ghost(self): # kad player pojede ghost-a, poziva ovu metodu
        self.eaten = True


