#kod za protivnike

# kod za protivnike
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
import player
from time import sleep
from math import sqrt, floor
from operator import itemgetter


class Enemy(QLabel):
    def __init__(self, label, map, player, scatter_target, ghost_id):
        super().__init__()

        self.label = label
        self.map = map
        self.player = player
        self.scatter_target = scatter_target # prosledjen Tuple, potrebno je ih pomnoziti sa 40 da bi se dobila pozicija na mapi
        self.ghost_id = ghost_id # ghost_id odredjuje koji kretajuci pattern prati
        self.eaten = False # da li ga je player pojeo
        self.activated_frightened = False
        self.reborned = False # da li se vratio ghost na pocetno mesto kad ga je pacman pojeo
        self.target_home = (400,400)
        self.mode = 0 # 0 - scatter mode
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
        self.previous_direction = 0 # 0 - dole
                                    # 1 - levo
                                    # 2 - gore
                                    # 3 - desno

    def move_chase(self): # ide za pacmanom
        pass

    def move_scatter(self): # ide u svoj ugao
        pass

    def move_frightened(self): # okrene se za 180 stepeni i random krece da se pomera
        pass

    def move_eaten(self): # vraca se na pocetnu poziciju, na 400 400
        self.move_to_target(self.reborned, self.check_if_ghost_returned_to_home, self.target_home)

    def move_to_target(self, uslov, uslov_za_izlazak, target): # Prima False uslov, metoda uslov_za_izlazak treba da postavi globalnu promenljivu i da vrati vrednost tu vrednost uslov promenljivi, kako bi se zavrsila ova metoda
        while not uslov:
            uslov = uslov_za_izlazak()
            pravac1 = (1,470)  # Maximum odstojanje je 466, pa ako se za neki pravac ne moze odrediti vrednost(napr. zid), nek ne utice na novi pravac
            pravac2 = (2, 470)
            pravac3 = (3, 470)
            if self.previous_direction == 0:  # pre isao ka dole
                if self.map.zid(self.label.x() - 40, self.label.y()):  # LEVO
                    pravac1 = (1, sqrt((abs(target[0] - (self.label.x() - 40)) ** 2) + (abs(target[1] - self.label.y()) ** 2)))
                if self.map.zid(self.label.x() + 40, self.label.y()):  # DESNO
                    pravac2 = (3, sqrt((abs(target[0] - (self.label.x() + 40)) ** 2) + (abs(target[1] - self.label.y()) ** 2)))
                if self.map.zid(self.label.x(), self.label.y() + 40):  # NASTAVI DOLE
                    pravac3 = (0, sqrt((abs(target[0] - (self.label.x())) ** 2) + (abs(target[1] - (self.label.y() + 40)) ** 2)))
                pravci = [pravac1, pravac3, pravac2]
                self.previous_direction = min(pravci, key=itemgetter(1))[0]
                self.move_to_direction(self.previous_direction)
                continue
            elif self.previous_direction == 1:  # pre isao ka LEVO
                if self.map.zid(self.label.x() - 40, self.label.y()):  # NASTAVI LEVO
                    pravac1 = (1, sqrt((abs(target[0] - (self.label.x() - 40)) ** 2) + (abs(target[1] - self.label.y()) ** 2)))
                if self.map.zid(self.label.x(), self.label.y() - 40):  # GORE
                    pravac2 = (2, sqrt((abs(target[0] - (self.label.x())) ** 2) + (abs(target[1] - (self.label.y() - 40)) ** 2)))
                if self.map.zid(self.label.x(), self.label.y() + 40):  # DOLE
                    pravac3 = (0, sqrt((abs(target[0] - (self.label.x())) ** 2) + (abs(target[1] - (self.label.y() + 40)) ** 2)))
                pravci = [pravac2, pravac1, pravac3]
                self.previous_direction = min(pravci, key=itemgetter(1))[0]  # tj. sledeci pravac
                self.move_to_direction(self.previous_direction)
                continue
            if self.previous_direction == 2:  # pre isao ka GORE
                if self.map.zid(self.label.x() - 40, self.label.y()):  # LEVO
                    pravac1 = (1, sqrt((abs(target[0] - (self.label.x() - 40)) ** 2) + (abs(target[1] - self.label.y()) ** 2)))
                if self.map.zid(self.label.x() + 40, self.label.y()):  # DESNO
                    pravac2 = (3, sqrt((abs(self.target_home[0] - (self.label.x() + 40)) ** 2) + (abs(self.target_home[1] - self.label.y()) ** 2)))
                if self.map.zid(self.label.x(), self.label.y() - 40):  # NASTAVI GORE
                    pravac3 = (2, sqrt((abs(target[0] - (self.label.x())) ** 2) + (abs(target[1] - (self.label.y() - 40)) ** 2)))
                pravci = [pravac3, pravac1, pravac2]
                self.previous_direction = min(pravci, key=itemgetter(1))[0]  # tj. sledeci pravac
                self.move_to_direction(self.previous_direction)
            if self.previous_direction == 3:  # pre isao ka DESNO
                if self.map.zid(self.label.x(), self.label.y() - 40):  # GORE
                    pravac1 = (2, sqrt((abs(target[0] - (self.label.x())) ** 2) + (abs(target[1] - (self.label.y() - 40)) ** 2)))
                if self.map.zid(self.label.x() + 40, self.label.y()):  # DESNO
                    pravac2 = (3, sqrt((abs(target[0] - (self.label.x() + 40)) ** 2) + (abs(target[1] - self.label.y()) ** 2)))
                if self.map.zid(self.label.x(), self.label.y() + 40):  # NASTAVI DOLE
                    pravac3 = (0, sqrt((abs(target[0] - (self.label.x())) ** 2) + (abs(target[1] - (self.label.y() + 40)) ** 2)))
                pravci = [pravac1, pravac3, pravac2]
                self.previous_direction = min(pravci, key=itemgetter(1))[0]  # tj. sledeci pravac
                self.move_to_direction(self.previous_direction)
                continue

    def check_if_ghost_returned_to_home(self): # Ako se vratio na pocetnu poziciju, rebornuje se
        if self.label.x() == self.target_home[0] and self.label.y() == self.target_home[1]:
            self.reborned = True
            return True

    def move_to_direction(self, direction):
        for i in range(2):
            if direction == 0: # DOLE
                self.change_look_of_ghost(1, 'Down')
                self.label.move(self.label.x(), self.label.y() + 20)
                #QGuiApplication.processEvents()
                sleep(0.05)
                self.change_look_of_ghost(2, 'Down')
                #QGuiApplication.processEvents()
                sleep(0.05)
            elif direction == 1: # LEVO
                self.change_look_of_ghost(1, 'Left')
                self.label.move(self.label.x() - 20, self.label.y())
                # QGuiApplication.processEvents()
                sleep(0.05)
                self.change_look_of_ghost(2, 'Left')
                # QGuiApplication.processEvents()
                sleep(0.05)
            elif direction == 2: # GORE
                self.change_look_of_ghost(1, 'Up')
                self.label.move(self.label.x(), self.label.y() - 20)
                # QGuiApplication.processEvents()
                sleep(0.05)
                self.change_look_of_ghost(2, 'Up')
                # QGuiApplication.processEvents()
                sleep(0.05)
            elif direction == 3: # DESNO
                self.change_look_of_ghost(1, 'Right')
                self.label.move(self.label.x() + 20, self.label.y())
                # QGuiApplication.processEvents()
                sleep(0.05)
                self.change_look_of_ghost(2, 'Right')
                # QGuiApplication.processEvents()
                sleep(0.05)

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

    def get_direction(self, enemy):
        pass

