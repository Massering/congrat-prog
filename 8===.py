import random
import sys

import pyautogui

from PyQt6.QtWidgets import *
from PyQt6 import QtCore, QtGui


class FakeDialog(QMainWindow):
    def __init__(self, screen):
        super().__init__()
        self.screen_width = screen.size().width()
        self.screen_height = screen.size().height()

        self.setWindowTitle(" ")
        self.setFixedSize(300, 100)
        self.setWindowFlags(QtCore.Qt.WindowType.CustomizeWindowHint |
                            QtCore.Qt.WindowType.WindowCloseButtonHint)

        self.label = QLabel("Ты самая красивая!", self)
        self.label.setGeometry(20, 10, 150, 30)

        self.yes_btn = QPushButton("Да", self)
        self.yes_btn.setGeometry(170, 50, 100, 30)
        self.yes_btn.clicked.connect(self.close)

        self.no_btn = QPushButton("Нет", self)
        self.no_btn.setGeometry(30, 50, 100, 30)
        self.no_btn.clicked.connect(self.close)
        self.no_btn.clicked.connect(lambda: success())


class RandomButtonDialog(FakeDialog):
    def __init__(self, screen):
        super().__init__(screen)

        def randomMoveEvent(event, sender, parent):
            new_x = random.randint(-(parent.screen_width // 4), parent.screen_width // 4)
            if random.randint(0, 1):
                new_x = random.randint(-(parent.screen_width // 8), parent.screen_width // 8)

            new_y = random.randint(-(parent.screen_height // 4), parent.screen_height // 4)
            if random.randint(0, 1):
                new_y = random.randint(-(parent.screen_height // 8), parent.screen_height // 8)

            sender.move(parent.pos().x() + parent.width() // 2 + new_x, parent.pos().y() + parent.height() // 2 + new_y)
            sender.moved = True

        self.no_btn.moved = False
        self.no_btn.enterEvent = lambda event: randomMoveEvent(event, self.no_btn, self)
        self.no_btn.setWindowFlags(2281762817 |    # Блять работает - не трожь
                                   QtCore.Qt.WindowType.WindowStaysOnTopHint |
                                   QtCore.Qt.WindowType.FramelessWindowHint)
        self.no_btn.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.no_btn.show()

    def moveEvent(self, event):
        if not self.no_btn.moved:
            self.no_btn.move(self.x() + 20, self.y() + 80)
        else:
            dx, dy = event.pos().x() - event.oldPos().x(), event.pos().y() - event.oldPos().y()
            self.no_btn.move(self.no_btn.x() + dx, self.no_btn.y() + dy)


class ChangingButtonDialog(FakeDialog):
    def __init__(self, screen):
        super().__init__(screen)

        def changeButtonsEvent(event, sender, parent):
            old_pos = sender.pos()
            sender.move(parent.yes_btn.x(), parent.yes_btn.y())
            parent.yes_btn.move(old_pos)

        self.no_btn.enterEvent = lambda event: changeButtonsEvent(event, self.no_btn, self)


class InactivatingButtonDialog(FakeDialog):
    def __init__(self, screen):
        super().__init__(screen)

        def inactivateButtonEvent(event, sender):
            sender.setEnabled(False)

        def activateButtonEvent(event, sender):
            sender.setEnabled(True)

        self.no_btn.enterEvent = lambda event: inactivateButtonEvent(event, self.no_btn)
        self.setMouseTracking(True)
        self.mouseMoveEvent = lambda event: activateButtonEvent(event, self.no_btn)


class DisappearingButtonDialog(FakeDialog):
    def __init__(self, screen):
        super().__init__(screen)

        self.yes_btn.setStyleSheet("background-color: rgba(253, 253, 253, 255);")
        self.setAnimated(True)

    def paintEvent(self, a0):
        # print('paintEvent')
        cur_x, cur_y = cursor_coordinates()
        btn_pos = self.mapToGlobal(self.no_btn.pos())
        btn_x1 = btn_pos.x()
        btn_x2 = btn_x1 + self.no_btn.width()
        btn_y1 = btn_pos.y()
        btn_y2 = btn_y1 + self.no_btn.height()

        dx = min(abs(btn_x1 - cur_x), abs(cur_x - btn_x2))
        dy = min(abs(btn_y1 - cur_y), abs(cur_y - btn_y2))

        if btn_x1 <= cur_x <= btn_x2:
            dx = 0
        if btn_y1 <= cur_y <= btn_y2:
            dy = 0

        r = round((dx ** 2 + dy ** 2) ** 0.5 * 3 - 10)

        k = max(min(r, 255), 1)  # *3 - уменьшение радиуса, -10 - ближе 10 пискелей значение 0
        if k == 1:  # 1 это схуяли-то 100%
            k = 0
        self.no_btn.setStyleSheet(
            f"color: rgba(0, 0, 0, {k});\n"
            f"background-color: rgba(253, 253, 253, {k});\n"
        )

        # чтобы тыки в невидимость не проходили
        if k <= 2:
            self.no_btn.setEnabled(False)
        else:
            self.no_btn.setEnabled(True)
        # бля ну и ладно todo

        super().paintEvent(a0)


class MovingToCursorDialog(FakeDialog):
    def __init__(self, screen):
        super().__init__(screen)

        self.setAnimated(True)
        self.setMouseTracking(True)
        self.label.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.no_btn.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)

    def paintEvent(self, a0):
        self.no_btn.setEnabled(False)
        self.no_btn.setEnabled(True)

        cur_x, cur_y = cursor_coordinates()

        btn_pos = self.mapToGlobal(self.yes_btn.pos())
        btn_x1 = btn_pos.x() + 4
        btn_x2 = btn_x1 + self.no_btn.width() - 8
        btn_y1 = btn_pos.y() + 4
        btn_y2 = btn_y1 + self.no_btn.height() - 8

        if cur_x < btn_x1:
            self.move(self.x() - (btn_x1 - cur_x), self.y())
        if cur_x >= btn_x2:
            self.move(self.x() + (cur_x - btn_x2), self.y())

        if cur_y < btn_y1:
            self.move(self.x(), self.y() - (btn_y1 - cur_y))
        if cur_y >= btn_y2:
            self.move(self.x(), self.y() + (cur_y - btn_y2))

        super().paintEvent(a0)


def cursor_coordinates():
    # todo: use pyqt functions instead of pyautogui
    return pyautogui.position()


def success():
    QMessageBox.warning(None, 'Ошибка', 'Успех!' + '\t' * 3)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Happy March 8th!")
        self.setFixedSize(400, 200)

        label = QLabel("""Поздравляем с 8 марта!
May all your dreams and aspirations come true!""")
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(label)


if __name__ == "__main__":
    app1 = QApplication(sys.argv)
    screen = QApplication.screens()[0]
    dlg1 = RandomButtonDialog(screen)
    dlg1.show()
    app1.exec()

    app2 = QApplication(sys.argv)
    dlg2 = ChangingButtonDialog(screen)
    dlg2.show()
    app2.exec()

    app3 = QApplication(sys.argv)
    dlg3 = InactivatingButtonDialog(screen)
    dlg3.show()
    app3.exec()

    app4 = QApplication(sys.argv)
    dlg4 = DisappearingButtonDialog(screen)
    dlg4.show()
    app4.exec()

    app5 = QApplication(sys.argv)
    dlg5 = MovingToCursorDialog(screen)
    dlg5.show()
    app5.exec()

    # All dialogs accepted, show main window
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
