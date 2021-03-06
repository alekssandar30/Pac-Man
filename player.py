
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap, QGuiApplication
from time import sleep
from enemy import Enemy
from random import randint
from threading import Thread


class Player(QLabel):
    def __init__(self, label, map, label_for_player_score, label_for_player_lifes, dead_label, start_position, player_id, player_name, player_speed, deus_ex_label, deus_ex_feedback_label):
        super().__init__()
        self.player_id = player_id
        self.player_name = player_name
        self.label = label
        self.map = map
        self.current_score = 0
        self.score_counter_label = label_for_player_score #QLabel(str(self.current_score)) Labela za score
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.provera = 0
        self.num_of_eated_ghost_powers = 0
        self.label_for_player_lifes = label_for_player_lifes
        self.player_lifes = 2 # 2 + 1 na mapi. | Ako padne na -1 onda je GAME OVERn
        self.reset_mode_for_enemies = -1
        self.in_reset = False
        self.dead_label = dead_label
        self.start_position = start_position
        self.player_speed = player_speed
        self.player_eated = False
        self.double_points_from_ex_machina = False
        self.deus_ex_label = deus_ex_label
        self.ghost_speed_up = False
        self.deus_ex_feedback_label = deus_ex_feedback_label
        if (player_id == 1):
            self.deus_ex_feedback_label.move(0,40)
        else:
            self.deus_ex_feedback_label.move(200,200)



    def return_num_of_eated_ghost_powers_by_player(self):
        return self.num_of_eated_ghost_powers

    #KRETANJE Pac Man-a
    def movePlayerLeft(self, label):
        self.left = True
        self.up = False
        self.down = False
        self.right = False
        if self.in_reset == False:
            if (self.provera == 1):
                while (True):
                    if (self.map.zid(label.x() - 40, label.y())):
                        break
                    if (self.map.zid(label.x(), label.y() - 20)):
                        label.setPixmap(QPixmap("images/PacManUpEat"+str(self.player_id)+".png"))
                        label.move(label.x(), label.y() - 20)
                        QGuiApplication.processEvents()
                        sleep(self.player_speed)
                        label.setPixmap(QPixmap("images/PacManUpClose"+str(self.player_id)+".png"))
                        QGuiApplication.processEvents()
                        sleep(self.player_speed)
                    elif (self.map.zid(label.x(), label.y() - 40)):
                        i = 0
                        while (i < 2):
                            label.setPixmap(QPixmap("images/PacManUpEat"+str(self.player_id)+".png"))
                            label.move(label.x(), label.y() - 20)
                            i += 1
                            if (i == 1):
                                if self.map.is_coin(label.x(), label.y() - 20):
                                    self.increase_points(10)
                                    self.map.draw_black_background(label.x(), label.y() - 20)
                                elif self.map.is_eat_ghosts_power(label.x(), label.y() - 20):
                                    # ovde ce da se ubrza pacman i da jede protivnike
                                    self.num_of_eated_ghost_powers += 1
                                    self.map.draw_black_background(label.x(), label.y() - 20)
                                elif self.map.is_deus_ex_machina_power(label.x(), label.y() - 20):
                                    self.map.draw_black_background(label.x(), label.y() - 20)
                                    self.start_deus_ex_thread()
                            QGuiApplication.processEvents()
                            sleep(self.player_speed)
                            label.setPixmap(QPixmap("images/PacManUpClose"+str(self.player_id)+".png"))
                            QGuiApplication.processEvents()
                            sleep(self.player_speed)
                    if (not self.map.zid(label.x() - 40, label.y()) and not self.map.zid(label.x(), label.y() - 40)):
                            break
            elif (self.provera == 3):
                while (True):
                    if (self.map.zid(label.x() - 40, label.y())):
                        break
                    if (self.map.zid(label.x(), label.y() + 20)):
                        label.setPixmap(QPixmap("images/PacManDownEat"+str(self.player_id)+".png"))
                        label.move(label.x(), label.y() + 20)
                        QGuiApplication.processEvents()
                        sleep(self.player_speed)
                        label.setPixmap(QPixmap("images/PacManDownClose"+str(self.player_id)+".png"))
                        QGuiApplication.processEvents()
                        sleep(self.player_speed)
                    elif (self.map.zid(label.x(), label.y() + 40)):
                        i = 0
                        while (i < 2):
                            label.setPixmap(QPixmap("images/PacManDownEat"+str(self.player_id)+".png"))
                            label.move(label.x(), label.y() + 20)
                            i += 1
                            if (i == 1):
                                if self.map.is_coin(label.x(), label.y() + 20):
                                    self.increase_points(10)
                                    self.map.draw_black_background(label.x(), label.y() + 20)
                                elif self.map.is_eat_ghosts_power(label.x(), label.y() + 20):
                                    # ovde ce da se ubrza pacman i da jede protivnike
                                    self.num_of_eated_ghost_powers += 1
                                    self.map.draw_black_background(label.x(), label.y() + 20)
                                elif self.map.is_deus_ex_machina_power(label.x(), label.y() + 20):
                                    self.map.draw_black_background(label.x(), label.y() + 20)
                                    self.start_deus_ex_thread()
                            QGuiApplication.processEvents()
                            sleep(self.player_speed)
                            label.setPixmap(QPixmap("images/PacManDownClose"+str(self.player_id)+".png"))
                            QGuiApplication.processEvents()
                            sleep(self.player_speed)
                    if (not self.map.zid(label.x() - 40, label.y()) and not self.map.zid(label.x(), label.y() + 40)):
                            break
            elif (self.provera == 4):
                while (True):
                    if (self.map.zid(label.x() - 40, label.y())):
                        break
                    if (self.map.zid(label.x() + 20, label.y())):
                        label.setPixmap(QPixmap("images/PacManRightEat"+str(self.player_id)+".png"))  # 760 320
                        if (label.x() == 760):
                            label.move(label.x() - 780, label.y())
                        else:
                            label.move(label.x() + 20, label.y())
                        QGuiApplication.processEvents()
                        sleep(self.player_speed)
                        label.setPixmap(QPixmap("images/PacManRightClose"+str(self.player_id)+".png"))
                        QGuiApplication.processEvents()
                        sleep(self.player_speed)
                    if (not self.map.zid(label.x() - 40, label.y()) and not self.map.zid(label.x() + 40, label.y())):
                            break
            self.provera = 2

            while (self.map.zid(label.x() - 40, label.y()) and self.left and self.up == False and self.down == False and self.right == False):
                self.up = False
                self.down = False
                self.right = False

                i = 0
                if (self.provera == 2):
                    label.setPixmap(QPixmap("images/PacManLeftEat"+str(self.player_id)+".png"))
                    if (label.x() == 0):
                        label.move(label.x() + 780, label.y())
                    else:
                        label.move(label.x() - 20, label.y())
                    i += 1
                    if (i == 1):
                        if self.map.is_coin(label.x() - 20, label.y()):
                            self.increase_points(10)
                            self.map.draw_black_background(label.x() - 20, label.y())
                        elif self.map.is_eat_ghosts_power(label.x() - 20, label.y()):
                            # ovde ce da se ubrza pacman i da jede protivnike
                            self.num_of_eated_ghost_powers += 1
                            self.map.draw_black_background(label.x() - 20, label.y())
                        elif self.map.is_deus_ex_machina_power(label.x() - 20, label.y()):
                            self.map.draw_black_background(label.x() - 20, label.y())
                            self.start_deus_ex_thread()
                    QGuiApplication.processEvents()
                    sleep(self.player_speed)
                    if (self.provera == 2):
                        label.setPixmap(QPixmap("images/PacManLeftClose"+str(self.player_id)+".png"))
                        QGuiApplication.processEvents()
                        sleep(self.player_speed)
                        if (self.map.zid(label.x() - 20, label.y())):
                            label.setPixmap(QPixmap("images/PacManLeftEat"+str(self.player_id)+".png"))
                            if (label.x() == 0):
                                label.move(label.x() + 780, label.y())
                            else:
                                label.move(label.x() - 20, label.y())
                            QGuiApplication.processEvents()
                            sleep(self.player_speed)
                            if (self.provera == 2):
                                label.setPixmap(QPixmap("images/PacManLeftClose"+str(self.player_id)+".png"))
                                QGuiApplication.processEvents()
                                sleep(self.player_speed)

    def movePlayerRight(self, label):
        self.right = True
        self.up = False
        self.down = False
        self.left = False
        if self.in_reset == False:
            if (self.provera == 1):
                while (True):
                    if (self.map.zid(label.x() + 40, label.y())):
                        break
                    if (self.map.zid(label.x(), label.y() - 20)):
                        label.setPixmap(QPixmap("images/PacManUpEat"+str(self.player_id)+".png"))
                        label.move(label.x(), label.y() - 20)
                        QGuiApplication.processEvents()
                        sleep(self.player_speed)
                        label.setPixmap(QPixmap("images/PacManUpClose"+str(self.player_id)+".png"))
                        QGuiApplication.processEvents()
                        sleep(self.player_speed)
                    elif (self.map.zid(label.x(), label.y() - 40)):
                        i = 0
                        while (i < 2):
                            label.setPixmap(QPixmap("images/PacManUpEat"+str(self.player_id)+".png"))
                            label.move(label.x(), label.y() - 20)
                            i += 1
                            if (i == 1):
                                if self.map.is_coin(label.x(), label.y() - 20):
                                    self.increase_points(10)
                                    self.map.draw_black_background(label.x(), label.y() - 20)
                                elif self.map.is_eat_ghosts_power(label.x(), label.y() - 20):
                                    # ovde ce da se ubrza pacman i da jede protivnike
                                    self.num_of_eated_ghost_powers += 1
                                    self.map.draw_black_background(label.x(), label.y() - 20)
                                elif self.map.is_deus_ex_machina_power(label.x(), label.y() - 20):
                                    self.start_deus_ex_thread()
                            QGuiApplication.processEvents()
                            sleep(self.player_speed)
                            label.setPixmap(QPixmap("images/PacManUpClose"+str(self.player_id)+".png"))
                            QGuiApplication.processEvents()
                            sleep(self.player_speed)
                    if (not self.map.zid(label.x() + 40, label.y()) and not self.map.zid(label.x(), label.y() - 40)):
                            break
            elif (self.provera == 3):
                while (True):
                    if (self.map.zid(label.x() + 40, label.y())):
                        break
                    if (self.map.zid(label.x(), label.y() + 20)):
                        label.setPixmap(QPixmap("images/PacManDownEat"+str(self.player_id)+".png"))
                        label.move(label.x(), label.y() + 20)
                        QGuiApplication.processEvents()
                        sleep(self.player_speed)
                        label.setPixmap(QPixmap("images/PacManDownClose"+str(self.player_id)+".png"))
                        QGuiApplication.processEvents()
                        sleep(self.player_speed)
                    elif (self.map.zid(label.x(), label.y() + 40)):
                        i = 0
                        while (i < 2):
                            label.setPixmap(QPixmap("images/PacManDownEat"+str(self.player_id)+".png"))
                            label.move(label.x(), label.y() + 20)
                            i += 1
                            if (i == 1):
                                if self.map.is_coin(label.x(), label.y() + 20):
                                    self.increase_points(10)
                                    self.map.draw_black_background(label.x(), label.y() + 20)
                                elif self.map.is_eat_ghosts_power(label.x(), label.y() + 20):
                                    # ovde ce da se ubrza pacman i da jede protivnike
                                    self.num_of_eated_ghost_powers += 1
                                    self.map.draw_black_background(label.x(), label.y() + 20)
                                elif self.map.is_deus_ex_machina_power(label.x(), label.y() + 20):
                                    self.map.draw_black_background(label.x(), label.y() + 10)
                                    self.start_deus_ex_thread()
                            QGuiApplication.processEvents()
                            sleep(self.player_speed)
                            label.setPixmap(QPixmap("images/PacManDownClose"+str(self.player_id)+".png"))
                            QGuiApplication.processEvents()
                            sleep(self.player_speed)
                    if (not self.map.zid(label.x() + 40, label.y()) and not self.map.zid(label.x(), label.y() + 40)):
                            break
            elif (self.provera == 2):
                while (True):
                    if (self.map.zid(label.x() + 40, label.y())):
                        break
                    if (self.map.zid(label.x() - 20, label.y())):
                        label.setPixmap(QPixmap("images/PacManLeftEat"+str(self.player_id)+".png"))
                        if (label.x() == 0):
                            label.move(label.x() + 780, label.y())
                        else:
                            label.move(label.x() - 20, label.y())
                        QGuiApplication.processEvents()
                        sleep(self.player_speed)
                        label.setPixmap(QPixmap("images/PacManLeftClose"+str(self.player_id)+".png"))
                        QGuiApplication.processEvents()
                        sleep(self.player_speed)
                    if (not self.map.zid(label.x() + 40, label.y()) and not self.map.zid(label.x() - 40, label.y())):
                            break
            self.provera = 4

            while (self.map.zid(label.x() + 40, label.y()) and self.right and self.up == False and self.down == False and self.left == False):
                self.up = False
                self.down = False
                self.left = False

                i = 0
                if (self.provera == 4):
                    label.setPixmap(QPixmap("images/PacManRightEat"+str(self.player_id)+".png")) #760 320
                    if (label.x() == 760):
                        label.move(label.x() - 780, label.y())
                    else:
                        label.move(label.x() + 20, label.y())
                    i += 1
                    if (i == 1):
                        if self.map.is_coin(label.x() + 20, label.y()):
                            self.increase_points(10)
                            self.map.draw_black_background(label.x() + 20, label.y())
                        elif self.map.is_eat_ghosts_power(label.x()+20, label.y()):
                            #ovde ce da se ubrza pacman i da jede protivnike
                            self.num_of_eated_ghost_powers += 1
                            self.map.draw_black_background(label.x()+20, label.y())
                        elif self.map.is_deus_ex_machina_power(label.x()+20, label.y()):
                            self.map.draw_black_background(label.x()+20, label.y())
                            self.start_deus_ex_thread()
                    QGuiApplication.processEvents()
                    sleep(self.player_speed)
                    if (self.provera == 4):
                        label.setPixmap(QPixmap("images/PacManRightClose"+str(self.player_id)+".png"))
                        QGuiApplication.processEvents()
                        sleep(self.player_speed)
                        if (self.map.zid(label.x() + 20, label.y())):
                            label.setPixmap(QPixmap("images/PacManRightEat"+str(self.player_id)+".png"))  # 760 320
                            if (label.x() == 760):
                                label.move(label.x() - 780, label.y())
                            else:
                                label.move(label.x() + 20, label.y())
                            QGuiApplication.processEvents()
                            sleep(self.player_speed)
                            if (self.provera == 4):
                                label.setPixmap(QPixmap("images/PacManRightClose"+str(self.player_id)+".png"))
                                QGuiApplication.processEvents()
                                sleep(self.player_speed)

    def movePlayerUp(self, label):
        #print("x = ", label.y(), " y = ", label.x(), " x[%20] = ", label.x() // 40, "y[%16] = ", label.y() // 40)
        self.up = True
        self.down = False
        self.left = False
        self.right = False
        if self.in_reset == False:
            if (self.provera == 2):
                while (True):
                    if (self.map.zid(label.x(), label.y() - 40)):
                        break
                    if (self.map.zid(label.x() - 20, label.y())):
                        label.setPixmap(QPixmap("images/PacManLeftEat"+str(self.player_id)+".png"))
                        if (label.x() == 0):
                            label.move(label.x() + 780, label.y())
                        else:
                            label.move(label.x() - 20, label.y())
                        QGuiApplication.processEvents()
                        sleep(self.player_speed)
                        label.setPixmap(QPixmap("images/PacManLeftClose"+str(self.player_id)+".png"))
                        QGuiApplication.processEvents()
                        sleep(self.player_speed)
                    elif (self.map.zid(label.x() - 40, label.y())):
                        i = 0
                        while (i < 2 and self.provera == 2):
                            label.setPixmap(QPixmap("images/PacManLeftEat"+str(self.player_id)+".png"))
                            if (label.x() == 0):
                                label.move(label.x() + 780, label.y())
                            else:
                                label.move(label.x() - 20, label.y())
                            i += 1
                            if (i == 1):
                                if self.map.is_coin(label.x() - 20, label.y()):
                                    self.increase_points(10)
                                    self.map.draw_black_background(label.x() - 20, label.y())
                                elif self.map.is_eat_ghosts_power(label.x() - 20, label.y()):
                                    # ovde ce da se ubrza pacman i da jede protivnike
                                    self.num_of_eated_ghost_powers += 1
                                    self.map.draw_black_background(label.x() - 20, label.y())
                                elif self.map.is_deus_ex_machina_power(label.x() - 20, label.y()):
                                    self.map.draw_black_background(label.x() - 20, label.y())
                                    self.start_deus_ex_thread()
                            QGuiApplication.processEvents()
                            sleep(self.player_speed)
                            label.setPixmap(QPixmap("images/PacManLeftClose"+str(self.player_id)+".png"))
                            QGuiApplication.processEvents()
                            sleep(self.player_speed)
                    if (not self.map.zid(label.x(), label.y() - 40) and not self.map.zid(label.x() - 40, label.y())):
                        break
            elif (self.provera == 3):
                while (True):
                    if (self.map.zid(label.x(), label.y() - 40)):
                        break
                    if (self.map.zid(label.x(), label.y() + 20)):
                        label.setPixmap(QPixmap("images/PacManDownEat"+str(self.player_id)+".png"))
                        label.move(label.x(), label.y() + 20)
                        QGuiApplication.processEvents()
                        sleep(self.player_speed)
                        label.setPixmap(QPixmap("images/PacManDownClose"+str(self.player_id)+".png"))
                        QGuiApplication.processEvents()
                        sleep(self.player_speed)
                    if (not self.map.zid(label.x(), label.y() - 40) and not self.map.zid(label.x(), label.y() + 40)):
                            break
            elif (self.provera == 4):
                while (True):
                    if (self.map.zid(label.x(), label.y() - 40)):
                        break
                    if (self.map.zid(label.x() + 20, label.y())):
                        label.setPixmap(QPixmap("images/PacManRightEat"+str(self.player_id)+".png"))  # 760 320
                        if (label.x() == 760):
                            label.move(label.x() - 780, label.y())
                        else:
                            label.move(label.x() + 20, label.y())
                        QGuiApplication.processEvents()
                        sleep(self.player_speed)
                        label.setPixmap(QPixmap("images/PacManRightClose"+str(self.player_id)+".png"))
                        QGuiApplication.processEvents()
                        sleep(self.player_speed)
                    elif (self.map.zid(label.x() + 40, label.y())):
                        i = 0
                        while (i < 2 and self.provera == 4):
                            label.setPixmap(QPixmap("images/PacManRightEat"+str(self.player_id)+".png"))  # 760 320
                            if (label.x() == 760):
                                label.move(label.x() - 780, label.y())
                            else:
                                label.move(label.x() + 20, label.y())
                            i += 1
                            if (i == 1):
                                if self.map.is_coin(label.x() + 20, label.y()):
                                    self.increase_points(10)
                                    self.map.draw_black_background(label.x() + 20, label.y())
                                elif self.map.is_eat_ghosts_power(label.x() + 20, label.y()):
                                    # ovde ce da se ubrza pacman i da jede protivnike
                                    self.num_of_eated_ghost_powers += 1
                                    self.map.draw_black_background(label.x() + 20, label.y())
                                elif self.map.is_deus_ex_machina_power(label.x() + 20, label.y()):
                                    self.map.draw_black_background(label.x() + 20, label.y())
                                    self.start_deus_ex_thread()
                            QGuiApplication.processEvents()
                            sleep(self.player_speed)
                            label.setPixmap(QPixmap("images/PacManRightClose"+str(self.player_id)+".png"))
                            QGuiApplication.processEvents()
                            sleep(self.player_speed)
                    if (not self.map.zid(label.x(), label.y() - 40) and not self.map.zid(label.x() + 40, label.y())):
                            break

            while (self.map.zid(label.x(), label.y() - 40) and self.up and self.down == False and self.right == False and self.left == False):
                self.down = False
                self.left = False
                self.right = False
                self.provera = 1

                i = 0
                if (self.provera == 1):
                    label.setPixmap(QPixmap("images/PacManUpEat"+str(self.player_id)+".png"))
                    label.move(label.x(), label.y() - 20)
                    i += 1
                    if (i == 1):
                        if self.map.is_coin(label.x(), label.y() - 20):
                            self.increase_points(10)
                            self.map.draw_black_background(label.x(), label.y() - 20)
                        elif self.map.is_eat_ghosts_power(label.x(), label.y() - 20):
                            # ovde ce da se ubrza pacman i da jede protivnike
                            self.num_of_eated_ghost_powers += 1
                            self.map.draw_black_background(label.x(), label.y() - 20)
                        elif self.map.is_deus_ex_machina_power(label.x(), label.y() - 20):
                            self.map.draw_black_background(label.x(), label.y() - 20)
                            self.start_deus_ex_thread()
                    QGuiApplication.processEvents()
                    sleep(self.player_speed)
                    if (self.provera == 1):
                        label.setPixmap(QPixmap("images/PacManUpClose"+str(self.player_id)+".png"))
                        QGuiApplication.processEvents()
                        sleep(self.player_speed)
                        if (self.map.zid(label.x(), label.y() - 20)):
                            label.setPixmap(QPixmap("images/PacManUpEat"+str(self.player_id)+".png"))
                            label.move(label.x(), label.y() - 20)
                            QGuiApplication.processEvents()
                            sleep(self.player_speed)
                            if (self.provera == 1):
                                label.setPixmap(QPixmap("images/PacManUpClose"+str(self.player_id)+".png"))
                                QGuiApplication.processEvents()
                                sleep(self.player_speed)

    def movePlayerDown(self, label):
        self.down = True
        self.up = False
        self.left = False
        self.right = False
        if self.in_reset == False:
            if (self.provera == 2):
                while (True):
                    if (self.map.zid(label.x(), label.y() + 40)):
                        break
                    if (self.map.zid(label.x() - 20, label.y())):
                        label.setPixmap(QPixmap("images/PacManLeftEat"+str(self.player_id)+".png"))
                        if (label.x() == 0):
                            label.move(label.x() + 780, label.y())
                        else:
                            label.move(label.x() - 20, label.y())
                        QGuiApplication.processEvents()
                        sleep(self.player_speed)
                        label.setPixmap(QPixmap("images/PacManLeftClose"+str(self.player_id)+".png"))
                        QGuiApplication.processEvents()
                        sleep(self.player_speed)
                    elif (self.map.zid(label.x() - 40, label.y())):
                        i = 0
                        while (i < 2 and self.provera == 2):
                            label.setPixmap(QPixmap("images/PacManLeftEat"+str(self.player_id)+".png"))
                            if (label.x() == 0):
                                label.move(label.x() + 780, label.y())
                            else:
                                label.move(label.x() - 20, label.y())
                            i += 1
                            if (i == 1):
                                if self.map.is_coin(label.x() - 20, label.y()):
                                    self.increase_points(10)
                                    self.map.draw_black_background(label.x() - 20, label.y())
                                elif self.map.is_eat_ghosts_power(label.x() - 20, label.y()):
                                    # ovde ce da se ubrza pacman i da jede protivnike
                                    self.num_of_eated_ghost_powers += 1
                                    self.map.draw_black_background(label.x() - 20, label.y())
                                elif self.map.is_deus_ex_machina_power(label.x() - 20, label.y()):
                                    self.map.draw_black_background(label.x() - 20, label.y())
                                    self.start_deus_ex_thread()
                            QGuiApplication.processEvents()
                            sleep(self.player_speed)
                            label.setPixmap(QPixmap("images/PacManLeftClose"+str(self.player_id)+".png"))
                            QGuiApplication.processEvents()
                            sleep(self.player_speed)
                    if (not self.map.zid(label.x(), label.y() + 40) and not self.map.zid(label.x() - 40, label.y())):
                        break
            elif (self.provera == 1):
                while (True):
                    if (self.map.zid(label.x(), label.y() + 40)):
                        break
                    if (self.map.zid(label.x(), label.y() - 20)):
                        label.setPixmap(QPixmap("images/PacManDownEat"+str(self.player_id)+".png"))
                        label.move(label.x(), label.y() - 20)
                        QGuiApplication.processEvents()
                        sleep(self.player_speed)
                        label.setPixmap(QPixmap("images/PacManDownClose"+str(self.player_id)+".png"))
                        QGuiApplication.processEvents()
                        sleep(self.player_speed)
                    if (not self.map.zid(label.x(), label.y() + 40) and not self.map.zid(label.x(), label.y() - 40)):
                            break
            elif (self.provera == 4):
                while (True):
                    if (self.map.zid(label.x(), label.y() + 40)):
                        break
                    if (self.map.zid(label.x() + 20, label.y())):
                        label.setPixmap(QPixmap("images/PacManRightEat"+str(self.player_id)+".png"))  # 760 320
                        if (label.x() == 760):
                            label.move(label.x() - 780, label.y())
                        else:
                            label.move(label.x() + 20, label.y())
                        QGuiApplication.processEvents()
                        sleep(self.player_speed)
                        label.setPixmap(QPixmap("images/PacManRightClose"+str(self.player_id)+".png"))
                        QGuiApplication.processEvents()
                        sleep(self.player_speed)
                    elif (self.map.zid(label.x() + 40, label.y())):
                        i = 0
                        while (i < 2 and self.provera == 4):
                            label.setPixmap(QPixmap("images/PacManRightEat"+str(self.player_id)+".png"))  # 760 320
                            if (label.x() == 760):
                                label.move(label.x() - 780, label.y())
                            else:
                                label.move(label.x() + 20, label.y())
                            i += 1
                            if (i == 1):
                                if self.map.is_coin(label.x() + 20, label.y()):
                                    self.increase_points(10)
                                    self.map.draw_black_background(label.x() + 20, label.y())
                                elif self.map.is_eat_ghosts_power(label.x() + 20, label.y()):
                                    # ovde ce da se ubrza pacman i da jede protivnike
                                    self.num_of_eated_ghost_powers += 1
                                    self.map.draw_black_background(label.x() + 20, label.y())
                                elif self.map.is_deus_ex_machina_power(label.x() + 20, label.y()):
                                    self.map.draw_black_background(label.x() + 20, label.y())
                                    self.start_deus_ex_thread()
                            QGuiApplication.processEvents()
                            sleep(self.player_speed)
                            label.setPixmap(QPixmap("images/PacManRightClose"+str(self.player_id)+".png"))
                            QGuiApplication.processEvents()
                            sleep(self.player_speed)
                    if (not self.map.zid(label.x(), label.y() + 40) and not self.map.zid(label.x() + 40, label.y())):
                            break

            while (self.map.zid(label.x(), label.y() + 40) and self.down and self.up == False and self.left == False and self.right == False):
                self.up = False
                self.left = False
                self.right = False
                self.provera = 3

                i = 0
                if (self.provera == 3):
                    label.setPixmap(QPixmap("images/PacManDownEat"+str(self.player_id)+".png"))
                    label.move(label.x(), label.y() + 20)
                    i += 1
                    if i == 1:
                        if self.map.is_coin(label.x(), label.y() + 20):
                            self.increase_points(10)
                            self.map.draw_black_background(label.x(), label.y() + 20)
                        elif self.map.is_eat_ghosts_power(label.x(), label.y() + 20):
                            # ovde ce da se ubrza pacman i da jede protivnike
                            self.num_of_eated_ghost_powers += 1
                            self.map.draw_black_background(label.x(), label.y() + 20)
                        elif self.map.is_deus_ex_machina_power(label.x(), label.y() + 20):
                            self.map.draw_black_background(label.x(), label.y() + 20)
                            self.start_deus_ex_thread()
                    QGuiApplication.processEvents()
                    sleep(self.player_speed)
                    if (self.provera == 3):
                        label.setPixmap(QPixmap("images/PacManDownClose"+str(self.player_id)+".png"))
                        QGuiApplication.processEvents()
                        sleep(self.player_speed)
                        if (self.map.zid(label.x(), label.y() + 20)):
                            label.setPixmap(QPixmap("images/PacManDownEat"+str(self.player_id)+".png"))
                            label.move(label.x(), label.y() + 20)
                            QGuiApplication.processEvents()
                            sleep(self.player_speed)
                            if (self.provera == 3):
                                label.setPixmap(QPixmap("images/PacManDownClose"+str(self.player_id)+".png"))
                                QGuiApplication.processEvents()
                                sleep(self.player_speed)

    def increase_points(self, points):
        if self.double_points_from_ex_machina == True:
            points *= 2
        self.current_score += points
        self.score_counter_label.setText(str(self.current_score))

    def return_current_player_position(self):
        return (self.label.x(), self.label.y())

    def increase_player_lifes(self):
        if self.player_lifes < 2:
            self.player_lifes += 1
            self.change_player_life_label()

    def decrease_player_lifes(self): # Poziva se reset
        self.player_lifes -= 1
        self.in_reset = False
        self.change_player_life_label()
        self.reset_mode_for_enemies = 4
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.provera = 0
        self.in_reset = True

    def change_player_life_label(self):
        if self.player_lifes == 0:
            self.label_for_player_lifes.setPixmap(QPixmap('images/ZeroLife.png'))
        elif self.player_lifes == 1:
            self.label_for_player_lifes.setPixmap(QPixmap('images/OneLife'+str(self.player_id)+'.png'))
        elif self.player_lifes == 2 or self.player_lifes > 2:
            self.label_for_player_lifes.setPixmap(QPixmap('images/TwoLife'+str(self.player_id)+'.png'))


    def return_reset_for_enemies(self):
        return self.reset_mode_for_enemies

    def set_reset_mode_from_enemy(self, mode):
        self.reset_mode_for_enemies = mode

    def start_deus_ex_thread(self):
        deus_ex_thread = Thread(target=self.deus_ex_machina_choose_randomly)
        deus_ex_thread.setDaemon(True)
        deus_ex_thread.start()

    def deus_ex_machina_choose_randomly(self): # 6 opcija: pacman ubrza, enemy ubrza, double coin, minus poeni, freeze, plus zivot. Pokrece se preko threda
        self.deus_ex_label.setHidden(True)
        self.deus_ex_feedback_label.setHidden(False)
        choice = randint(1,6)
        if choice == 1: # pacman ubrza
            self.player_speed = 0.05
            self.change_deus_ex_image_for_seconds(8, 'FeedbackPacmanSpeedUp')
            self.player_speed = 0.07
        elif choice == 2: # enemy ubrza
            self.ghost_speed_up = True
            self.change_deus_ex_image_for_seconds(4, 'FeedbackSpeedUpEnemy')
            self.ghost_speed_up = False
        elif choice == 3: # double coin
            self.double_points_from_ex_machina = True
            self.change_deus_ex_image_for_seconds(10, 'FeedbackDoubleCoin')
            self.double_points_from_ex_machina = False
        elif choice == 4: # minnus poeni
            minus_score = randint(10,100)
            if self.current_score - minus_score >= 0:
                 self.current_score -= minus_score
            else:
                  self.current_score = 0
            self.change_deus_ex_image_for_seconds(4, 'FeedbackCoinLose')
        elif choice == 5: # freeze
            self.player_speed = 3
            self.change_deus_ex_image_for_seconds(2, 'FeedbackPlayerFreeze')
            self.player_speed = 0.07
        elif choice == 6: # plus zivot
            self.increase_player_lifes()
            self.change_deus_ex_image_for_seconds(8, 'FeedbackPlusLife')

        self.deus_ex_feedback_label.setHidden(True)

    def change_deus_ex_image_for_seconds(self, seconds, image):
        seconds = seconds // 2
        for _ in range(seconds):
            self.deus_ex_feedback_label.setPixmap(QPixmap('images/'+image+'.png'))
            sleep(1)
            self.deus_ex_feedback_label.setPixmap(QPixmap('images/'+image+'1.png'))
            sleep(1)