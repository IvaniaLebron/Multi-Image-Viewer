import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import Qt

class CheckerboardDisplayApp(QWidget):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle('Image Display')
        self.setGeometry(100, 100, 400, 400)

        # Create a label to display the white screen
        self.label = QLabel(self)
        self.label.setScaledContents(True)  # Enable scaling of the label's content
        self.display_white_screen()

        # Create a button for saving the image
        self.save_button = QPushButton('Save Image', self)
        self.save_button.clicked.connect(self.save_image)

        # Set up the layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.save_button)
        self.setLayout(layout)

    def display_white_screen(self):
        # Create a white image
        white_image = QPixmap(400, 400)
        white_image.fill(QColor(Qt.white))
        self.label.setPixmap(white_image)

    def save_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG Files (*.png);;JPEG Files (*.jpg)",
                                                   options=options)
        if file_path:
            # Save the white image
            self.label.pixmap().save(file_path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CheckerboardDisplayApp()
    window.show()
    sys.exit(app.exec_())