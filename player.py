#kod za kretanje igraca, sakupljanje poena...
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap


class Player(QLabel):
    def __init__(self, label, map, label_for_player_score):
        super().__init__()
        self.label = label
        self.map = map
        self.current_score = 0
        self.score_counter_label = label_for_player_score #QLabel(str(self.current_score)) Labela za score

    #KRETANJE Pac Man-a
    def movePlayerLeft(self, label):
        if self.map.is_tunnel(label.x() - 40, label.y()) or self.map.is_coin(label.x() - 40, label.y()) or self.map.is_eat_ghosts_power(label.x() - 40, label.y()):
            label.setPixmap(QPixmap("images/PacManLeftEat.png"))
            label.move(label.x() - 40, label.y())


    def movePlayerRight(self, label):
        if self.map.is_tunnel(label.x() + 40, label.y()) or self.map.is_coin(label.x() + 40, label.y() or self.map.is_eat_ghosts_power(label.x() +40, label.y())):
            label.setPixmap(QPixmap("images/PacManRightEat.png"))
            label.move(label.x() + 40, label.y())

    def movePlayerUp(self, label):
        #print("x = ", label.y(), " y = ", label.x(), " x[%20] = ", label.x() // 40, "y[%16] = ", label.y() // 40)
        if self.map.is_tunnel(label.x(), label.y() - 40) or self.map.is_coin(label.x(), label.y() - 40) or self.map.is_eat_ghosts_power(label.x(), label.y() - 40):
            label.setPixmap(QPixmap("images/PacManUpEat.png"))
            label.move(label.x(), label.y() - 40)

    def movePlayerDown(self, label):
        if self.map.is_tunnel(label.x(), label.y() + 40) or self.map.is_coin(label.x() , label.y() + 40) or self.map.is_eat_ghosts_power(label.x(), label.y() + 40):
            label.setPixmap(QPixmap("images/PacManDownEat.png"))
            label.move(label.x(), label.y() + 40)

    #funkcije za setovanje pixmape playera
    def set_left_close(self, label):
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
        label.setPixmap(QPixmap("images/PacManDownClose.png"))

    def increase_points(self, points):
        self.current_score += points
        self.score_counter_label.setText(str(self.current_score))







