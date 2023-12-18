import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QLineEdit, QFileDialog
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from checkerboard_display import CheckerboardDisplayApp
from grid_display import GridDisplayApp

class SelectImagesApp(QWidget):
    def __init__(self, effect, default_images):
        super().__init__()
        self.display_window = None
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

        # Change to an input field for square size
        self.square_size_input = QLineEdit(self)
        self.square_size_input.setPlaceholderText("Enter size of squares (in pixels)")
        self.square_size_input.setVisible(effect == 'CheckerBoard Effect')
        layout.addWidget(self.square_size_input)
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

            if self.effect == 'CheckerBoard Effect':
                if len(selected_files) == 2:
                    try:
                        square_size = int(self.square_size_input.text())
                    except ValueError:
                        QMessageBox.information(self, 'Error', 'Invalid square size', QMessageBox.Ok)
                        return
                    # Open the CheckerboardDisplayApp with the selected images and square size
                    self.display_window = CheckerboardDisplayApp(selected_files[0], selected_files[1], square_size)
                    self.display_window.show()
                else:
                    QMessageBox.information(self, 'Error', 'Please select exactly 2 images for Checkerboard Effect',
                                            QMessageBox.Ok)
            elif self.effect == 'Grid Effect':
                # Open the Grid App with selected grid layout
                rows_and_columns = int(np.sqrt(self.default_images))
                if len(selected_files) == self.default_images:
                    self.display_window = GridDisplayApp(selected_files, rows_and_columns,
                                                    rows_and_columns)
                    self.display_window.show()
                else:
                    QMessageBox.information(self, 'Error', f'Please select exactly {self.default_images} images for your selected Grid Display', QMessageBox.Ok)
            else:
                # Code for the other option
                QMessageBox.information(self, 'Error', 'Please select a valid option', QMessageBox.Ok)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    effect = 'CheckerBoard Effect'
    default_images = 2
    window = SelectImagesApp(effect, default_images)
    window.show()
    sys.exit(app.exec_())

