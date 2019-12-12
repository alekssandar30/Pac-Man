#kod za kretanje igraca, sakupljanje poena...
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap
from time import sleep
from PyQt5 import QtGui
import threading
from queue import Queue


class Player(QLabel):
    def __init__(self, label, map, label_for_player_score):
        super().__init__()
        self.label = label
        self.map = map
        self.current_score = 0
        self.score_counter_label = label_for_player_score #QLabel(str(self.current_score)) Labela za score
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.pomoc = 0

    #KRETANJE Pac Man-a
    def movePlayerLeft(self, label):
        self.left = True
        while (self.map.is_tunnel(label.x() - 40, label.y()) or self.map.is_coin(label.x() - 40, label.y()) or self.map.is_eat_ghosts_power(label.x() - 40, label.y())) and self.left:
            self.up = False
            self.down = False
            self.right = False
            i = 0
            while (i < 2):
                self.up = False
                self.down = False
                self.right = False
                label.setPixmap(QPixmap("images/PacManLeftEat.png"))
                label.move(label.x() - 20, label.y())
                QtGui.QGuiApplication.processEvents()
                sleep(0.03)
                label.setPixmap(QPixmap("images/PacManLeftClose.png"))
                QtGui.QGuiApplication.processEvents()
                sleep(0.03)
                i += 1
                if (i == 2):
                    if self.map.is_coin(label.x(), label.y()):
                        self.increase_points(10)
                    self.map.draw_black_background(label.x(), label.y())
                    QtGui.QGuiApplication.processEvents()

    def movePlayerRight(self, label):
        self.right = True
        while (self.map.is_tunnel(label.x() + 40, label.y()) or self.map.is_coin(label.x() + 40, label.y() or self.map.is_eat_ghosts_power(label.x() +40, label.y()))) and self.right:
            self.up = False
            self.down = False
            self.left = False
            i = 0
            while (i < 2):
                label.setPixmap(QPixmap("images/PacManRightEat.png"))
                label.move(label.x() + 20, label.y())
                QtGui.QGuiApplication.processEvents()
                sleep(0.03)
                label.setPixmap(QPixmap("images/PacManRightClose.png"))
                QtGui.QGuiApplication.processEvents()
                sleep(0.03)
                i += 1
                if (i == 2):
                    if self.map.is_coin(label.x(), label.y()):
                        self.increase_points(10)
                    self.map.draw_black_background(label.x(), label.y())
                    QtGui.QGuiApplication.processEvents()

    def movePlayerUp(self, label):
        #print("x = ", label.y(), " y = ", label.x(), " x[%20] = ", label.x() // 40, "y[%16] = ", label.y() // 40)
        self.up = True
        while (self.map.is_tunnel(label.x(), label.y() - 40) or self.map.is_coin(label.x(), label.y() - 40) or self.map.is_eat_ghosts_power(label.x(), label.y() - 40)) and self.up:
            self.down = False
            self.left = False
            self.right = False
            i = 0
            while (i < 2):
                self.down = False
                self.left = False
                self.right = False
                label.setPixmap(QPixmap("images/PacManUpEat.png"))
                label.move(label.x(), label.y() - 20)
                QtGui.QGuiApplication.processEvents()
                sleep(0.03)
                label.setPixmap(QPixmap("images/PacManUpClose.png"))
                QtGui.QGuiApplication.processEvents()
                sleep(0.03)
                i += 1
                if (i == 2):
                    if self.map.is_coin(label.x(), label.y()):
                        self.increase_points(10)
                    self.map.draw_black_background(label.x(), label.y())
                    QtGui.QGuiApplication.processEvents()

    def movePlayerDown(self, label):
        self.down = True
        while (self.map.is_tunnel(label.x(), label.y() + 40) or self.map.is_coin(label.x() , label.y() + 40) or self.map.is_eat_ghosts_power(label.x(), label.y() + 40)) and self.down:
            self.up = False
            self.left = False
            self.right = False
            i = 0
            while (i < 2):
                label.setPixmap(QPixmap("images/PacManDownEat.png"))
                label.move(label.x(), label.y() + 20)
                QtGui.QGuiApplication.processEvents()
                sleep(0.03)
                label.setPixmap(QPixmap("images/PacManDownClose.png"))
                QtGui.QGuiApplication.processEvents()
                sleep(0.03)
                i += 1
                if (i == 2):
                    if self.map.is_coin(label.x(), label.y()):
                        self.increase_points(10)
                    self.map.draw_black_background(label.x(), label.y())
                    QtGui.QGuiApplication.processEvents()

    #funkcije za setovanje pixmape playera
    '''def set_left_close(self, label):
        #if (label.x() % 40)+20 == 20:
        if self.map.is_coin(label.x(), label.y()):
            self.increase_points(10)
        self.map.draw_black_background(label.x(), label.y())
        label.setPixmap(QPixmap("images/PacManLeftClose.png"))

    def set_right_close(self, label):
        #if (label.x() % 40)+20 == 30:
        if self.map.is_coin(label.x(), label.y()):
            self.increase_points(10)
        self.map.draw_black_background(label.x(), label.y())
        label.setPixmap(QPixmap("images/PacManRightClose.png"))

    def set_up_close(self, label):
        #if (label.y() % 40)+20 == 20:
        if self.map.is_coin(label.x(), label.y()):
            self.increase_points(10)
        self.map.draw_black_background(label.x(), label.y())
        label.setPixmap(QPixmap("images/PacManUpClose.png"))

    def set_down_close(self, label):
        #if (label.y() % 40)+20 == 30:
        if self.map.is_coin(label.x(), label.y()):
            self.increase_points(10)
        self.map.draw_black_background(label.x(), label.y())
        label.setPixmap(QPixmap("images/PacManDownClose.png"))'''

    def increase_points(self, points):
        self.current_score += points
        self.score_counter_label.setText(str(self.current_score))







