import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QLineEdit, QFileDialog
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from checkerboard_display import CheckerboardDisplayApp
from grid_display import ImageGridApp
class SelectImagesApp(QWidget):
    def __init__(self, effect, default_images):
        super().__init__()
        self.effect = effect
        self.default_images = default_images

        # Set window properties
        self.setWindowTitle(f'Select Images for {effect}')
        self.setGeometry(100, 100, 600, 300)

        # Create widgets
        label = QLabel(f'Select {default_images} images for {effect}:', self)
        self.style_label(label)

        hint_label = QLabel('(Click "Select Images" to choose)', self)
        self.style_hint_label(hint_label)

        btn_select_images = QPushButton('Select Images', self)
        btn_select_images.clicked.connect(self.select_images)
        self.style_button(btn_select_images)

        # Set up the layout
        layout = QVBoxLayout(self)
        layout.addWidget(label, alignment=Qt.AlignCenter)
        layout.addWidget(hint_label, alignment=Qt.AlignCenter)
        layout.addWidget(btn_select_images)

        self.setLayout(layout)

    def style_label(self, label):
        label.setStyleSheet("font-size: 20px; margin-bottom: 10px; color: #333;")

    def style_hint_label(self, hint_label):
        hint_label.setStyleSheet("font-size: 14px; color: #777; margin-bottom: 20px;")

    def style_button(self, button):
        button.setStyleSheet("font-size: 16px; padding: 15px; margin: 10px; background-color: #3498db; color: white; border: 2px solid #2980b9; border-radius: 8px;")

    def select_images(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        options |= QFileDialog.HideNameFilterDetails

        file_dialog = QFileDialog()
        file_dialog.setOptions(options)
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("Images (*.png *.xpm *.jpg *.jpeg *.bmp)")

        if file_dialog.exec_() == QFileDialog.Accepted:
            selected_files = file_dialog.selectedFiles()

            if self.effect == 'Grid Effect':
                #the user should select the grid 2x2, 3x3, 4x4
                #This should get the selected rows and columns by the user, work on that, asking and getting okkkk
                    #maybe 3 buttons would be best for this approach
                    self.display_window = ImageGridApp(selected_files,2,2)
                    self.display_window.show()
            elif self.effect == 'CheckerBoard Effect':
                if len(selected_files) == 2:
                    # Open the CheckerboardDisplayApp with the selected images
                    self.display_window = CheckerboardDisplayApp(selected_files[0], selected_files[1])
                    self.display_window.show()
                else:
                    QMessageBox.information(self, 'Error', 'Please select exactly 2 images', QMessageBox.Ok)
            else:
                #code for the other option
                QMessageBox.information(self, 'Error', 'Please select valid option', QMessageBox.Ok)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    effect = 'Grid Effect'
    default_images = 2
    window = SelectImagesApp(effect, default_images)
    window.show()
    sys.exit(app.exec_())
