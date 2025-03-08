import random
import sys
import os

import pyautogui
from PyQt6.QtGui import QRegion

from PyQt6.QtWidgets import *
from PyQt6 import QtCore, QtGui


def resource_path(relative_path) -> str:
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    print(os.path.join(base_path, relative_path))
    return str(os.path.join(base_path, relative_path))


class FakeDialog(QMainWindow):
    def __init__(self, nice_text):
        super().__init__()

        self.setWindowTitle(" ")
        self.setFixedSize(300, 100)
        self.setWindowFlags(QtCore.Qt.WindowType.CustomizeWindowHint |
                            QtCore.Qt.WindowType.WindowCloseButtonHint)

        self.label = QLabel(nice_text, self)
        self.label.setGeometry(20, 10, 260, 30)

        self.yes_btn = QPushButton("Да", self)
        self.yes_btn.setGeometry(170, 50, 100, 30)
        self.yes_btn.clicked.connect(self.close)

        self.no_btn = QPushButton("Нет", self)
        self.no_btn.setGeometry(30, 50, 100, 30)
        self.no_btn.clicked.connect(self.close)
        self.no_btn.clicked.connect(lambda: success())


class RandomButtonDialog(FakeDialog):
    def __init__(self, nice_text):
        super().__init__(nice_text)

        self.screen_width, self.screen_height = pyautogui.size()

        def randomMoveEvent(event, sender, parent):
            rw = parent.screen_width // 4
            new_x = random.randint(-rw, rw)
            if random.randint(0, 1):
                new_x = random.randint(-(rw // 2), rw // 2)

            rh = parent.screen_height // 4
            new_y = random.randint(-rh, rh)
            if random.randint(0, 1):
                new_y = random.randint(-(rh // 2), rh // 2)

            sender.move(parent.pos().x() + parent.width() // 2 + new_x, parent.pos().y() + parent.height() // 2 + new_y)
            sender.moved = True

        self.no_btn.moved = False
        self.no_btn.enterEvent = lambda event: randomMoveEvent(event, self.no_btn, self)
        self.no_btn.setWindowFlags(2281762817 |  # Блять работает - не трожь
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
    def __init__(self, nice_text):
        super().__init__(nice_text)

        def changeButtonsEvent(event, sender, parent):
            old_pos = sender.pos()
            sender.move(parent.yes_btn.x(), parent.yes_btn.y())
            parent.yes_btn.move(old_pos)

        self.no_btn.enterEvent = lambda event: changeButtonsEvent(event, self.no_btn, self)


class InactivatingButtonDialog(FakeDialog):
    def __init__(self, nice_text):
        super().__init__(nice_text)

        def inactivateButtonEvent(event, sender):
            sender.setEnabled(False)

        def activateButtonEvent(event, sender):
            sender.setEnabled(True)

        self.no_btn.enterEvent = lambda event: inactivateButtonEvent(event, self.no_btn)
        self.setMouseTracking(True)
        self.mouseMoveEvent = lambda event: activateButtonEvent(event, self.no_btn)


class DisappearingButtonDialog(FakeDialog):
    def __init__(self, nice_text):
        super().__init__(nice_text)

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

        r = round((dx ** 2 + dy ** 2) ** 0.5)
        # *3 - уменьшение радиуса, -10 - ближе 10 пискелей значение 0
        r = r * 6 - 10

        k = max(min(r, 255), 1)
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
    def __init__(self, nice_text):
        super().__init__(nice_text)

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


class VoidCircleDialog(FakeDialog):
    def __init__(self, nice_text):
        super().__init__(nice_text)

    def paintEvent(self, a0):
        self.no_btn.setEnabled(False)
        self.no_btn.setEnabled(True)

        cur_pos = self.mapFromGlobal(QtCore.QPoint(*cursor_coordinates()))
        cur_x, cur_y = cur_pos.x(), cur_pos.y()

        d = 39

        for item in [self.no_btn, self.label]:
            item_rect = QtCore.QRect(0, 0, item.width(), item.height())
            item_cur_circle = QtCore.QRect(cur_x - item.x() - d // 2, cur_y - item.y() - d // 2, d, d)

            item_reg = QtGui.QRegion(item_rect, QRegion.RegionType.Rectangle)
            item_cur_reg = QtGui.QRegion(item_cur_circle, QtGui.QRegion.RegionType.Ellipse)

            item.setMask(item_reg.subtracted(item_cur_reg))

        super().paintEvent(a0)


def cursor_coordinates():
    # todo: use pyqt functions instead of pyautogui
    return pyautogui.position()


def success():
    QMessageBox.warning(None, 'Ошибка', 'Успех!' + '\t' * 3)


class MainWindow(QMainWindow):
    def __init__(self, nice_text, picture=None):
        super().__init__()
        self.setWindowTitle("С 8 марта!")

        layout = QVBoxLayout(self)
        label = QLabel(nice_text, self)
        label.setStyleSheet("font-size: 18px; \nmargin: 20px")
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        if picture:
            pic = QLabel(self)
            pic.setPixmap(picture)
            pic.setScaledContents(True)
            layout.addWidget(pic)

        layout.setSpacing(30)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


if __name__ == "__main__":
    # pyinstaller --onefile --noconsole --icon=icon.png --add-data "C:/Projects/pets/8march/icon.png;." 8===.py
    app = QApplication(sys.argv)

    icon_pixmap = QtGui.QPixmap(resource_path("icon.png"))
    icon = QtGui.QIcon(icon_pixmap)

    for dlg_type, text in [
        (DisappearingButtonDialog, 'Ты самая красивая!'),
        (MovingToCursorDialog, 'Ты самая умная!'),
        (ChangingButtonDialog, 'Ты самая яркая!'),
        (VoidCircleDialog, 'Ты самая добрая!'),
        (RandomButtonDialog, 'Ты самая лучшая!')
    ]:
        dlg = dlg_type(text)
        dlg.setWindowIcon(icon)
        dlg.show()
        app.exec()

    # All dialogs accepted, show main window
    window = MainWindow("""Поздравляю с 8 марта!
Пусть все мечты сбываются! 
Будь счастлива и всегда улыбайся!""",
                        icon_pixmap)
    window.setWindowIcon(icon)
    window.show()
    app.exec()
