import sys
import os

from PyQt6 import QtWidgets, QtGui

from mainwindow import MainWindow
from dialogs import (DisappearingButtonDialog, MovingToCursorDialog,
                     ChangingButtonDialog, VoidCircleDialog, RandomButtonDialog)


def resource_path(relative_path) -> str:
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    # print(os.path.join(base_path, relative_path))
    return str(os.path.join(base_path, relative_path))


if __name__ == "__main__":
    # pyinstaller --onefile --noconsole --icon=icon.png --add-data "C:/Projects/pets/8march/icon.png;." --name="c 8 марта" main.py
    app = QtWidgets.QApplication(sys.argv)

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
