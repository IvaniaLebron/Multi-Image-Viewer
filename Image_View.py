import glob
import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QFileDialog, QMessageBox
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
        self.next_button.clicked.connect(lambda: self.change_image(1))
        self.next_button.setGeometry(760, 280, 40, 40)

        self.prev_button = QPushButton("<", self)
        self.prev_button.clicked.connect(lambda: self.change_image(-1))
        self.prev_button.setGeometry(0, 280, 40, 40)

        self.image_folder = None
        self.image_files = []
        self.current_image_index = -1
        self.animations = []  # Keep references to animations

        self.select_image_folder()

    def select_image_folder(self):
        while True:
            folder = QFileDialog.getExistingDirectory(self, "Select Image Folder")

            # Check if the user canceled the folder selection
            if not folder:
                break
            # Check if the folder contains any image files
            image_extensions = ["*.png", "*.jpg", "*.jpeg", "*.bmp", "*.gif"]
            image_files = []
            for extension in image_extensions:
                image_files.extend(glob.glob(os.path.join(folder, extension)))
            if not image_files:
                # No images found in the folder, show a message box and restart the loop
                QMessageBox.warning(self, "No Images", "Please select a folder which has images.")
            else:
                # Images found, set the folder and load images
                self.image_folder = folder
                self.load_images(folder)
                self.show_image(0)
                break  # Exit the loop since a valid folder has been selected

    def load_images(self, folder):
        self.image_files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
        self.image_files.sort()

    def show_image(self, index):
        if 0 <= index < len(self.image_files):
            image_path = os.path.join(self.image_folder, self.image_files[index])
            pixmap = QPixmap(image_path)
            self.current_label.setPixmap(pixmap.scaled(800, 600, Qt.KeepAspectRatio, Qt.FastTransformation))
            self.current_image_index = index

    def change_image(self, direction):
        new_index = self.current_image_index + direction
        if 0 <= new_index < len(self.image_files):
            next_image_path = os.path.join(self.image_folder, self.image_files[new_index])
            next_pixmap = QPixmap(next_image_path)
            self.next_label.setPixmap(next_pixmap.scaled(800, 600, Qt.KeepAspectRatio, Qt.FastTransformation))
            self.prepare_next_image(new_index)
            self.start_animation(direction)
            self.current_image_index = new_index

    def prepare_next_image(self, new_index):
        next_image_path = os.path.join(self.image_folder, self.image_files[new_index])
        next_pixmap = QPixmap(next_image_path)
        self.next_label.setPixmap(next_pixmap.scaled(800, 600, Qt.KeepAspectRatio, Qt.FastTransformation))
        self.next_label.lower()  # Ensure this label is behind the current_label

    def start_animation(self, direction):
        current_end_pos = QRect(-800 if direction > 0 else 800, 0, 800, 600)
        next_start_pos = QRect(0, 0, 800, 600)
        next_end_pos = QRect(-800 if direction > 0 else 800, 0, 800, 600)

        self.animate_label(self.current_label, self.current_label.geometry(), current_end_pos)
        self.next_label.setGeometry(next_start_pos)
        self.animate_label(self.next_label, next_start_pos, QRect(0, 0, 800, 600))

        self.current_label, self.next_label = self.next_label, self.current_label

    def animate_label(self, label, start_rect, end_rect):
        animation = QPropertyAnimation(label, b"geometry")
        animation.setDuration(1000)
        animation.setStartValue(start_rect)
        animation.setEndValue(end_rect)
        animation.start()

        self.animations.append(animation)
        animation.finished.connect(lambda: self.animations.remove(animation))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageViewApp()
    window.show()
    sys.exit(app.exec_())
