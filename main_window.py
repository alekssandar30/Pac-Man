#Ovde ce biti kod za lavirint

from PyQt5.QtWidgets import QGraphicsView, QLabel


class MainWindow(QGraphicsView):

    def __init__(self):
        super().__init__()

        self.width = 650
        self.height = 500

        self.score = 0
        self.score_label = QLabel('Score: ', self)

        self.init_ui()

        self.show()

    def init_ui(self):

        self.setWindowTitle('Pac-Man')
        self.setFixedWidth(self.width)
        self.setFixedHeight(self.height)

        self.score_label.move(5, 15)

