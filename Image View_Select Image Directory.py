import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QPropertyAnimation, QTimer

class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()
        
        # List to hold paths of images in the selected directory
        self.image_paths = []
        self.current_index = 0
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.image_label = QLabel()
        self.layout.addWidget(self.image_label)

        self.prev_button = QPushButton('Previous')
        self.prev_button.clicked.connect(self.show_previous_image)
        
        self.next_button = QPushButton('Next')
        self.next_button.clicked.connect(self.show_next_image)

        # Horizontal layout to arrange the buttons
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.prev_button)
        self.button_layout.addWidget(self.next_button)

        self.layout.addLayout(self.button_layout)

        self.setLayout(self.layout)

        self.select_image_directory()

    def select_image_directory(self):
        options = QFileDialog.Options()
        directory = QFileDialog.getExistingDirectory(self, "Select Image Directory", options=options)
        if directory:
            self.image_paths = [os.path.join(directory, file) for file in os.listdir(directory)
                                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
            if self.image_paths:
                self.show_image(self.current_index)

    def show_image(self, index):
        pixmap = QPixmap(self.image_paths[index])
        self.image_label.setPixmap(pixmap.scaledToWidth(800))
        self.image_label.setAlignment(Qt.AlignCenter)

    def show_previous_image(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.slide_images("right")

    def show_next_image(self):
        if self.current_index < len(self.image_paths) - 1:
            self.current_index += 1
            self.slide_images("left")

    def slide_images(self, direction):
        start_value = self.image_label.geometry()
        end_value = start_value.translated(-self.width() if direction == "left" else self.width(), 0)

         # Create a property animation for sliding effect
        animation = QPropertyAnimation(self.image_label, b"geometry")
        animation.setDuration(300)
        animation.setStartValue(start_value)
        animation.setEndValue(end_value)

        animation.start()
        QTimer.singleShot(300, lambda: self.show_image(self.current_index))

def main():
    app = QApplication(sys.argv)
    viewer = ImageViewer()
    viewer.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


