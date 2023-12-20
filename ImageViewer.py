import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QPropertyAnimation, QRect, Qt

class ImageViewApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Image Viewer')
        self.setGeometry(100, 100, 800, 600)

        self.current_label = QLabel(self)
        self.current_label.setGeometry(0, 0, 800, 600)
        self.current_label.setScaledContents(True)

        self.next_label = QLabel(self)
        self.next_label.setGeometry(800, 0, 800, 600)  # Start off-screen
        self.next_label.setScaledContents(True)

        self.next_button = QPushButton(">", self)
        self.next_button.setGeometry(760, 280, 40, 40)

        self.prev_button = QPushButton("<", self)
        self.prev_button.setGeometry(0, 280, 40, 40)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageViewApp()
    window.show()
    sys.exit(app.exec_())