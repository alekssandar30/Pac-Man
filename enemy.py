#kod za protivnike

# kod za protivnike
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
import player


class Enemy(QLabel):
    def __init__(self, label, map, player):
        super().__init__()

        self.label = label
        self.map = map
        self.player = player


        #self.enemies = [self.blue_enemy, self.orange_enemy, self.red_enemy, self.rose_enemy, self.yellow_enemy]

        self.up = False
        self.down = False
        self.left = False
        self.right = False



    # move
    # imacu jednu metodu move koja ce "pametno" da poziva metode za kretanje
    # iz playera...

    def get_direction(self, enemy):
        pass

