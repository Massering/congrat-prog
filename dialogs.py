import random

from PyQt6 import QtWidgets, QtCore, QtGui


class FakeDialog(QtWidgets.QMainWindow):
    def __init__(self, nice_text):
        super().__init__()

        self.setWindowTitle(" ")
        self.setFixedSize(300, 100)
        self.setWindowFlags(QtCore.Qt.WindowType.CustomizeWindowHint |
                            QtCore.Qt.WindowType.WindowCloseButtonHint)

        self.label = QtWidgets.QLabel(nice_text, self)
        self.label.setGeometry(20, 10, 260, 30)

        self.yes_btn = QtWidgets.QPushButton("Да", self)
        self.yes_btn.setGeometry(170, 50, 100, 30)
        self.yes_btn.clicked.connect(self.close)

        self.no_btn = QtWidgets.QPushButton("Нет", self)
        self.no_btn.setGeometry(30, 50, 100, 30)
        self.no_btn.clicked.connect(self.close)
        self.no_btn.clicked.connect(success)


class RandomButtonDialog(FakeDialog):
    def __init__(self, nice_text):
        super().__init__(nice_text)

        screen_size = QtWidgets.QApplication.primaryScreen().size()
        self.screen_width, self.screen_height = screen_size.width(), screen_size.height()

        self.no_btn.enterEvent = self.random_move_no_btn
        self.no_btn.setWindowFlags(QtCore.Qt.WindowType.Window |
                                   QtCore.Qt.WindowType.FramelessWindowHint)
        self.no_btn.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.no_btn.show()

    def moveEvent(self, event):
        dx, dy = event.pos().x() - event.oldPos().x(), event.pos().y() - event.oldPos().y()
        self.no_btn.move(self.no_btn.x() + dx, self.no_btn.y() + dy)

    def random_move_no_btn(self, event):
        rw = self.screen_width // 4
        new_x = random.randint(-rw, rw)

        rh = self.screen_height // 4
        new_y = random.randint(-rh, rh)
        if random.randint(0, 1):
            new_x = random.randint(-(rw // 2), rw // 2)
            new_y = random.randint(-(rh // 2), rh // 2)

        self.no_btn.move(self.pos().x() + self.width() // 2 + new_x,
                         self.pos().y() + self.height() // 2 + new_y)


class ChangingButtonDialog(FakeDialog):
    def __init__(self, nice_text):
        super().__init__(nice_text)

        self.no_btn.enterEvent = self.change_buttons

    def change_buttons(self, event):
        old_pos = self.no_btn.pos()
        self.no_btn.move(self.yes_btn.x(), self.yes_btn.y())
        self.yes_btn.move(old_pos)


class DisappearingButtonDialog(FakeDialog):
    def __init__(self, nice_text):
        super().__init__(nice_text)

        self.no_btn.setWindowFlags(QtCore.Qt.WindowType.Window |
                                   QtCore.Qt.WindowType.FramelessWindowHint)
        self.no_btn.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.no_btn.show()

    def moveEvent(self, event):
        dx, dy = event.pos().x() - event.oldPos().x(), event.pos().y() - event.oldPos().y()
        self.no_btn.move(self.no_btn.x() + dx, self.no_btn.y() + dy)

    def paintEvent(self, a0):
        self.yes_btn.setEnabled(True)

        cur_x, cur_y = cursor_coordinates()
        btn_pos = self.no_btn.pos()
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
        off = 5  # - ближе off пискелей значение 0
        coef = 3  # - уменьшение большего радиуса в coef раз
        k = (r - off) * coef

        k = max(min(k, 100), 0) / 100
        self.no_btn.setWindowOpacity(k)

        QtWidgets.QApplication.postEvent(self, QtGui.QPaintEvent(QtCore.QRect()))


class MovingToCursorDialog(FakeDialog):
    def __init__(self, nice_text):
        super().__init__(nice_text)

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

        QtWidgets.QApplication.postEvent(self, QtGui.QPaintEvent(QtCore.QRect()))


class VoidCircleDialog(FakeDialog):
    def __init__(self, nice_text):
        super().__init__(nice_text)

    def paintEvent(self, a0):
        cur_pos = self.mapFromGlobal(QtCore.QPoint(*cursor_coordinates()))
        cur_x, cur_y = cur_pos.x(), cur_pos.y()

        d = 39

        for item in [self.no_btn, self.label]:
            item_rect = QtCore.QRect(0, 0, item.width(), item.height())
            item_cur_circle = QtCore.QRect(cur_x - item.x() - d // 2, cur_y - item.y() - d // 2, d, d)

            item_reg = QtGui.QRegion(item_rect, QtGui.QRegion.RegionType.Rectangle)
            item_cur_reg = QtGui.QRegion(item_cur_circle, QtGui.QRegion.RegionType.Ellipse)

            item.setMask(item_reg.subtracted(item_cur_reg))

        QtWidgets.QApplication.postEvent(self, QtGui.QPaintEvent(QtCore.QRect()))


def cursor_coordinates():
    return QtGui.QCursor.pos().x(), QtGui.QCursor.pos().y()


def success():
    QtWidgets.QMessageBox.warning(None, 'Ошибка', 'Успех!' + '\t' * 3)
