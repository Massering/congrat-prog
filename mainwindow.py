from PyQt6 import QtWidgets, QtCore


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, nice_text, picture=None):
        super().__init__()
        self.setWindowTitle("С 8 марта!")

        layout = QtWidgets.QVBoxLayout(self)
        label = QtWidgets.QLabel(nice_text, self)
        label.setStyleSheet("font-size: 18px")
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        if picture:
            pic = QtWidgets.QLabel(self)
            pic.setPixmap(picture)
            pic.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(pic)

        layout.setSpacing(30)
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
