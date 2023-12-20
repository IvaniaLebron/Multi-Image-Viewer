import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox, QSlider
from PyQt5.QtGui import QPixmap, QPainter, QImage
from PyQt5.QtCore import Qt

class ImageComparatorApp(QWidget):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle('Image Comparator')
        self.setGeometry(100, 100, 800, 600)

        # Create a button for selecting images
        self.select_images_button = QPushButton('Select Images', self)
        self.select_images_button.clicked.connect(self.select_images)

        # Create a slider for adjusting the reveal of the image
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.valueChanged[int].connect(self.adjust_image)
        self.slider.hide()

        # Create a label to display the images
        self.label = QLabel(self)
        self.label.setScaledContents(True)

        # Set up the layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.slider)
        layout.addWidget(self.select_images_button)
        self.setLayout(layout)

    def select_images(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("Images (*.png *.xpm *.jpg)")
        if file_dialog.exec_() == QFileDialog.Accepted:
            selected_files = file_dialog.selectedFiles()
            if len(selected_files) == 2:
                self.display_images(selected_files[0], selected_files[1])
            else:
                QMessageBox.information(self, 'Error', 'Please select exactly 2 images', QMessageBox.Ok)

    def display_images(self, image_path1, image_path2):
        self.image1 = QPixmap(image_path1)
        self.image2 = QPixmap(image_path2)

        # Use dimensions of the larger image for display
        self.width = max(self.image1.width(), self.image2.width())
        self.height = max(self.image1.height(), self.image2.height())

        self.setGeometry(100, 100, self.width, self.height + self.slider.height() + 10)
        self.slider.setMaximum(self.width)
        self.slider.setValue(self.width // 2)
        self.slider.show()

        self.update_image()

    def update_image(self):
        composite_image = QImage(self.width, self.height, QImage.Format_ARGB32)
        composite_image.fill(Qt.transparent)

        painter = QPainter(composite_image)

        # Draw the bottom image
        painter.drawPixmap(0, 0, self.image1)

        # Draw the top image, cut off at the slider's position
        top_image_cropped = self.image2.copy(0, 0, self.slider.value(), self.height).scaled(self.slider.value(), self.height, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        painter.drawPixmap(0, 0, top_image_cropped)

        painter.end()

        self.label.setPixmap(QPixmap.fromImage(composite_image))

    def adjust_image(self, value):
        self.update_image()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageComparatorApp()
    window.show()
    sys.exit(app.exec_())
