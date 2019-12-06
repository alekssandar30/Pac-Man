#kod za kretanje igraca, sakupljanje poena...
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap


class Player(QLabel):
    def __init__(self, label, map):
        super().__init__()
        self.label = label
        self.map = map

    #KRETANJE Pac Man-a
    def movePlayerLeft(self, label):
        #print("x = " , label.y() , " y = " ,label.x()," x[%20] = " ,label.x()//40 ,"y[%16] = " , label.y()//40)
        if self.map.is_tunnel(label.x() - 10, label.y()):
            label.setPixmap(QPixmap("images/PacManLeftEat.png"))
            label.move(label.x() - 10, label.y())

    def movePlayerRight(self, label):
        if self.map.is_tunnel(label.x() + 30, label.y()): # +30 potrebno da PacMan ne bi "usao" svojom polovinom u zid.
            label.setPixmap(QPixmap("images/PacManRightEat.png"))
            label.move(label.x() + 10, label.y())

    def movePlayerUp(self, label):
        if self.map.is_tunnel(label.x(), label.y() - 10):
            label.setPixmap(QPixmap("images/PacManUpEat.png"))
            label.move(label.x(), label.y() - 10)

    def movePlayerDown(self, label):
        if self.map.is_tunnel(label.x(), label.y() + 30): # +30 potrebno da PacMan ne bi "usao" svojom polovinom u zid.
            label.setPixmap(QPixmap("images/PacManDownEat.png"))
            label.move(label.x(), label.y() + 10)

    #funkcije za setovanje pixmape playera
    def set_left_close(self, label):
        label.setPixmap(QPixmap("images/PacManLeftClose.png"))

    def set_right_close(self, label):
        label.setPixmap(QPixmap("images/PacManRightClose.png"))

    def set_up_close(self, label):
        label.setPixmap(QPixmap("images/PacManUpClose.png"))

    def set_down_close(self, label):
        label.setPixmap(QPixmap("images/PacManDownClose.png"))






