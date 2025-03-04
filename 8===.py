import sys

from PyQt6.QtGui import QRegion, QPalette
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt6 import QtCore, QtGui, QtWidgets


class BeautyDialog(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Question 1")
        self.resize(300, 100)
        # self.setFixedSize(300, 200)

        # screen = QApplication.screens()[0]
        # print(screen.geometry(), screen.size())
        # sw, sh = screen.size().width(), screen.size().height()
        # self.move(sw // 2 - self.width() // 2, sh // 2 - self.height() // 2)

        rect = QtCore.QRect(-5000, -5000, 10000, 10000)
        my_region = QtGui.QRegion(rect, QtGui.QRegion.RegionType.Rectangle)
        self.setMask(my_region)

        # layout = QVBoxLayout()
        label = QLabel("Ты самая красивая!", self)
        label.move(20, 20)
        yes_btn = QPushButton("Да", self)
        yes_btn.setGeometry(140, 50, 100, 30)
        yes_btn.clicked.connect(self.close)

        self.no_btn = QPushButton("Нет")
        self.no_btn.setGeometry(self.x() + 20, self.y() + 50, 100, 30)
        self.no_btn.clicked.connect(self.close)
        self.no_btn.enterEvent = randomMoveEventFabric(self.no_btn)

        self.no_btn.setWindowFlags(self.windowFlags() |
                                   Qt.WindowType.WindowStaysOnTopHint |
                                   Qt.WindowType.FramelessWindowHint)
        self.no_btn.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.no_btn.show()
        self.no_btn.setFocus()
        # layout.addWidget(label)
        # layout.addWidget(yes_btn)
        # print(no_btn.enterEvent)
        # no_btn.setWindowFlags(Qt.WindowType)

        # layout.addWidget(label)
        # layout.addWidget(yes_btn)
        # layout.addWidget(no_btn)
        # self.setLayout(layout)

    def closeEvent(self, a0):
        print('close event')
        self.no_btn.close()
        self.close()

    def moveEvent(self, a1):
        print('move event')
        self.no_btn.move(self.x() + 20, self.y() + 50)
        self.no_btn.show()
        # self.no_btn.se


def randomMoveEventFabric(sender):
    old_enter_event = sender.enterEvent

    def randomMoveEvent(event, sender):
        sender.move(sender.x(), sender.y() + 50)
        old_enter_event(event)

    return lambda event: randomMoveEvent(event, sender)


class SmartDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Question 2")
        layout = QVBoxLayout()
        label = QLabel("Ты самая умная!")
        yes_btn = QPushButton("Yes")
        no_btn = QPushButton("No")

        yes_btn.clicked.connect(self.accept)
        no_btn.clicked.connect(self.reject)

        layout.addWidget(label)
        layout.addWidget(yes_btn)
        layout.addWidget(no_btn)
        self.setLayout(layout)


class BestDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Question 3")
        layout = QVBoxLayout()
        label = QLabel("Ты самая лучшая!")
        yes_btn = QPushButton("Yes")
        no_btn = QPushButton("No")

        yes_btn.clicked.connect(self.accept)
        no_btn.clicked.connect(self.reject)

        layout.addWidget(label)
        layout.addWidget(yes_btn)
        layout.addWidget(no_btn)
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Happy March 8th!")
        self.setGeometry(100, 100, 400, 200)

        label = QLabel("""Поздравляем с 8 марта!
May all your dreams and aspirations come true!""")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(label)


if __name__ == "__main__":
    app1 = QApplication(sys.argv)
    dlg1 = BeautyDialog()
    # dlg1.showMaximized()
    dlg1.show()
    app1.exec()

    app2 = QApplication(sys.argv)
    dlg2 = BeautyDialog()
    dlg2.show()
    app2.exec()

    # dlg3 = BestDialog()
    # dlg3.exec()

    # All dialogs accepted, show main window
    app3 = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app3.exec()
