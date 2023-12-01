import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap, QImage, QPainter, QBrush, QColor
from PyQt5.QtCore import Qt, QRect

class CheckerboardDisplayApp(QWidget):
    def __init__(self, image_path1, image_path2):
        super().__init__()

        self.image1 = QPixmap(image_path1)
        self.image2 = QPixmap(image_path2)

        # Set window properties
        self.setWindowTitle('Checkerboard Image Display')
        self.setGeometry(100, 100, 600, 600)

        # Create a label to display the checkerboard image
        self.label = QLabel(self)
        self.display_checkerboard()

        # Set up the layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def display_checkerboard(self):
        # Create a new QPixmap to hold the checkerboard pattern
        checkerboard = QPixmap(600, 600)
        checkerboard.fill(Qt.white)
        painter = QPainter(checkerboard)

        # Calculate the size of each checkerboard square
        square_size = min(self.image1.width(), self.image1.height(), self.image2.width(), self.image2.height()) // 8

        for row in range(8):
            for col in range(8):
                rect = QRect(col * square_size, row * square_size, square_size, square_size)
                if (row + col) % 2 == 0:
                    painter.drawPixmap(rect, self.image1, rect)
                else:
                    painter.drawPixmap(rect, self.image2, rect)

        painter.end()
        self.label.setPixmap(checkerboard)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CheckerboardDisplayApp('path_to_image1.jpg', 'path_to_image2.jpg')  # Replace with actual paths
    window.show()
    sys.exit(app.exec_())
