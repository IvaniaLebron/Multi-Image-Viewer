import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox, \
    QSizePolicy
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt, QRect

class CheckerboardDisplayApp(QWidget):
    def __init__(self, image_path1, image_path2, square_size):
        super().__init__()
        
        # Check if exactly two images have been provided
        if not image_path1 or not image_path2:
            raise ValueError("Exactly two images must be provided")

        # Check that square_size is a positive number
        if not isinstance(square_size, int) or square_size <= 0:
            raise ValueError("square_size must be a positive integer")
            
        self.image1 = QPixmap(image_path1)
        self.image2 = QPixmap(image_path2)
        self.square_size = square_size

        # Use dimensions of the larger image for the checkerboard
        self.checkerboard_width = max(self.image1.width(), self.image2.width())
        self.checkerboard_height = max(self.image1.height(), self.image2.height())

        # Set window properties
        self.setWindowTitle('Checkerboard Image Display')
        self.setGeometry(100, 100, self.checkerboard_width, self.checkerboard_height)

        # Create a label to display the checkerboard image
        self.label = QLabel(self)
        self.label.setScaledContents(True)  # Enable scaling of the label's content
        self.original_pixmap = self.display_checkerboard(self.checkerboard_width, self.checkerboard_height)
        self.label.setPixmap(self.original_pixmap)

        # Set minimum size for label to allow shrinking
        self.label.setMinimumSize(1, 1)

        # Set size policy to allow dynamic expanding and shrinking
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Create a button for saving the image
        self.save_button = QPushButton('Save Image', self)
        self.save_button.clicked.connect(self.save_image)

        # Set up the layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.save_button)
        self.setLayout(layout)
        self.user_resizing = True

    def display_checkerboard(self, width, height):
        # Create a new QPixmap to hold the checkerboard pattern
        checkerboard = QPixmap(width, height)
        checkerboard.fill(Qt.white)
        painter = QPainter(checkerboard)

        # Draw a basic checkerboard
        for row in range(0, height, self.square_size):
            for col in range(0, width, self.square_size):
                rect = QRect(col, row, self.square_size, self.square_size)

                # Decide wich image to use for this square
                image_to_use = self.image1 if (row // self.square_size + col // self.square_size) % 2 == 0 else self.image2

                source_x = min((image_to_use.width() // (width // self.square_size)) * (col // self.square_size),
                               image_to_use.width() - self.square_size)
                source_y = min((image_to_use.height() // (height // self.square_size)) * (row // self.square_size),
                               image_to_use.height() - self.square_size)
                source_rect = QRect(source_x, source_y, self.square_size, self.square_size)

                painter.drawPixmap(rect, image_to_use, source_rect)

        painter.end()
        return checkerboard

    def resizeEvent(self, event):
        # Resize the window to maintain a square aspect ratio
        new_dimension = min(self.width(), self.height())
        self.resize(new_dimension, new_dimension)
        if self.user_resizing:
            new_dimension = min(self.width(), self.height())
            self.label.resize(new_dimension, new_dimension)
            scaled_pixmap = self.original_pixmap.scaled(new_dimension, new_dimension, Qt.IgnoreAspectRatio,
                                                        Qt.FastTransformation)
            self.label.setPixmap(scaled_pixmap)
            self.user_resizing = False
        else:
            self.user_resizing = True

        super().resizeEvent(event)

    def save_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "JPEG Files (*.jpg);;PNG Files (*.png)",
                                                   options=options)
        if file_path:
            self.label.pixmap().save(file_path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CheckerboardDisplayApp('path_to_image1.jpg', 'path_to_image2.jpg',8)  # Replace with actual paths and number of squares
    window.show()
    sys.exit(app.exec_())
