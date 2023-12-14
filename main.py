import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from Select_Image import SelectImagesApp
from grid_select import GridSelector

class ImageViewerApp(QWidget):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle('Image Viewer and Manipulator')
        self.setGeometry(100, 100, 600, 400)

        # Create widgets
        label = QLabel('Choose an Operation:', self)
        self.style_label(label)

        btn_checkerboard = QPushButton('View Image', self)
        btn_checkerboard.clicked.connect(lambda: self.show_option_selected('View Image'))
        self.style_button(btn_checkerboard)

        btn_image_view = QPushButton('CheckerBoard Effect', self)
        btn_image_view.clicked.connect(lambda: self.show_option_selected('CheckerBoard Effect'))
        self.style_button(btn_image_view)

        btn_grid = QPushButton('Grid Effect', self)
        btn_grid.clicked.connect(lambda: self.show_option_selected('Grid Effect'))
        self.style_button(btn_grid)

        # Set up the layout
        layout = QVBoxLayout(self)
        layout.addWidget(label, alignment=Qt.AlignCenter)
        layout.addWidget(btn_checkerboard)
        layout.addWidget(btn_image_view)
        layout.addWidget(btn_grid)

        self.setLayout(layout)

    def style_label(self, label):
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 20px; margin-bottom: 20px; color: #333;")

    def style_button(self, button):
        button.setStyleSheet("font-size: 16px; padding: 15px; margin: 10px; background-color: #3498db; color: white; border: 2px solid #2980b9; border-radius: 8px;")

    def show_option_selected(self, option):
        if option == 'CheckerBoard Effect':
            #Open the SelectImagesApp window
            self.image_selector = SelectImagesApp('CheckerBoard Effect', 1)
            self.image_selector.show()
        elif option == 'Grid Effect':
            self.image_selector = GridSelector()
            self.image_selector.show()
        else:
            QMessageBox.information(self, 'Option Selected', f'You selected: {option}', QMessageBox.Ok)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageViewerApp()
    window.show()
    sys.exit(app.exec_())
