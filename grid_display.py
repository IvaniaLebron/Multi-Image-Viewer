import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QGridLayout, QSizePolicy, QLayout
from PyQt5.QtGui import QPixmap, QMouseEvent, QImage, QPainter
from PyQt5.QtCore import Qt, QEvent
from PIL import Image
import os

class ImageGridApp(QWidget):
    def __init__(self, image_paths, rows, cols):
        super().__init__()

        self.image_paths = image_paths
        self.rows = rows
        self.cols = cols

        self.images = []
        for path in self.image_paths:
            pixmap = QPixmap(path)
            self.images.append(pixmap)

        self.initUI()

    def initUI(self):
        grid_layout = QGridLayout()
        self.setLayout(grid_layout)

        self.labels = []  # To keep references to labels for later updates
        for i in range(self.rows):
            for j in range(self.cols):
                label = ClickableLabel(self, i, j)
                label.setPixmap(self.images[(i * self.cols + j) % len(self.images)])
                grid_layout.addWidget(label, i, j)
                self.labels.append(label)

        self.setWindowTitle(f"Image Grid ({self.rows}x{self.cols})")
        self.show()

class ClickableLabel(QLabel):
    def __init__(self, parent, row, col):
        super().__init__(parent)
        self.row = row
        self.col = col

    def mousePressEvent(self, event):
        # Handle mouse click event
        if event.button() == Qt.LeftButton:
            # Zoom in on the clicked image and all others in the same position
            for label in self.parent().labels:
                if label.row == self.row and label.col == self.col:
                    label.setScaledContents(True)
                    label.setFixedSize(200, 200)  # Set the desired size for zoomed images
                else:
                    label.setScaledContents(False)
                    label.setFixedSize(100, 100)  # Reset the size for other images

if __name__ == '__main__':
    app = QApplication(sys.argv)

    image_paths = ['path_to_image1.jpg', 'path_to_image2.jpg', 'path_to_image3.jpg', 'path_to_image4.jpg']
    rows = 2
    cols = 2

    window = ImageGridApp(image_paths, rows, cols)
    sys.exit(app.exec_())