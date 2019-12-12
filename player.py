#kod za kretanje igraca, sakupljanje poena...
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap, QGuiApplication
from time import sleep


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

    #KRETANJE Pac Man-a
    def movePlayerLeft(self, label):
        self.left = True
        while (self.map.zid(label.x() - 40, label.y()) and self.left):
            self.up = False
            self.down = False
            self.right = False
            i = 0
            while (i < 2):
                label.setPixmap(QPixmap("images/PacManLeftEat.png"))
                if (label.x() == 0):
                    label.move(label.x() + 780, label.y())
                    QGuiApplication.processEvents()
                else:
                    label.move(label.x() - 20, label.y())
                    QGuiApplication.processEvents()
                sleep(0.05)
                label.setPixmap(QPixmap("images/PacManLeftClose.png"))
                QGuiApplication.processEvents()
                sleep(0.05)
                i += 1
                if (i == 1):
                    if self.map.is_coin(label.x() - 20, label.y()):
                        self.increase_points(10)
                        self.map.draw_black_background(label.x() - 20, label.y())
                    elif self.map.is_eat_ghosts_power(label.x()-20, label.y()):
                        #ovde ce da se ubrza pacman i da jede protivnike
                        self.map.draw_black_background(label.x()-20, label.y())

                    QGuiApplication.processEvents()


    def movePlayerRight(self, label):
        self.right = True
        while (self.map.zid(label.x() +40, label.y()) and self.right):
            self.up = False
            self.down = False
            self.left = False
            i = 0
            while (i < 2):
                label.setPixmap(QPixmap("images/PacManRightEat.png")) #760 320
                if (label.x() == 760):
                    label.move(label.x() - 780, label.y())
                    QGuiApplication.processEvents()
                else:
                    label.move(label.x() + 20, label.y())
                    QGuiApplication.processEvents()
                sleep(0.05)
                label.setPixmap(QPixmap("images/PacManRightClose.png"))
                QGuiApplication.processEvents()
                sleep(0.05)
                i += 1
                if (i == 1):
                    if self.map.is_coin(label.x() + 20, label.y()):
                        self.increase_points(10)
                        self.map.draw_black_background(label.x() + 20, label.y())
                    elif self.map.is_eat_ghosts_power(label.x()+20, label.y()):
                        #ovde ce da se ubrza pacman i da jede protivnike
                        self.map.draw_black_background(label.x()+20, label.y())

                    QGuiApplication.processEvents()

    def movePlayerUp(self, label):
        #print("x = ", label.y(), " y = ", label.x(), " x[%20] = ", label.x() // 40, "y[%16] = ", label.y() // 40)
        self.up = True
        while (self.map.zid(label.x(), label.y() - 40) and self.up):
            self.down = False
            self.left = False
            self.right = False
            i = 0
            while (i < 2):
                label.setPixmap(QPixmap("images/PacManUpEat.png"))
                label.move(label.x(), label.y() - 20)
                QGuiApplication.processEvents()
                sleep(0.05)
                label.setPixmap(QPixmap("images/PacManUpClose.png"))
                QGuiApplication.processEvents()
                sleep(0.05)
                i += 1
                if (i == 1):
                    if self.map.is_coin(label.x(), label.y() - 20):
                        self.increase_points(10)
                        self.map.draw_black_background(label.x(), label.y() - 20)
                    elif self.map.is_eat_ghosts_power(label.x(), label.y()-20):
                        #ovde ce da se ubrza pacman i da jede protivnike
                        self.map.draw_black_background(label.x(), label.y()-20)

                    QGuiApplication.processEvents()

    def movePlayerDown(self, label):
        self.down = True
        while (self.map.zid(label.x(), label.y() + 40) and self.down):
            self.up = False
            self.left = False
            self.right = False
            i = 0
            while (i < 2):
                label.setPixmap(QPixmap("images/PacManDownEat.png"))
                label.move(label.x(), label.y() + 20)
                QGuiApplication.processEvents()
                sleep(0.05)
                label.setPixmap(QPixmap("images/PacManDownClose.png"))
                QGuiApplication.processEvents()
                sleep(0.05)
                i += 1
                if i == 1:
                    if self.map.is_coin(label.x(), label.y() + 20):
                        self.increase_points(10)
                        self.map.draw_black_background(label.x(), label.y() + 20)
                    elif self.map.is_eat_ghosts_power(label.x(), label.y()+20):
                        #ovde ce da se ubrza pacman i da jede protivnike
                        self.map.draw_black_background(label.x(), label.y()+20)

                    QGuiApplication.processEvents()

    def increase_points(self, points):
        self.current_score += points
        self.score_counter_label.setText(str(self.current_score))

    def ispis(self):
        i = 0
        while (i < 5):
            print("zdravo")
            i += 1







