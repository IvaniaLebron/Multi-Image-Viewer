import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class GridSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.selection = ''

        self.setWindowTitle('Select your preferred grid view')
        self.setGeometry(100, 100, 600, 300)

        # Create widgets
        label = QLabel('Select your preferred grid view', self)
        self.style_label(label)

        hint_label = QLabel('(You can choose a 2x2, 3x3 and 4x4 grid)', self)
        self.style_hint_label(hint_label)

        btn2x2 = QPushButton('2x2', self)
        btn2x2.clicked.connect(lambda: self.change_selection('2x2'))
        self.style_button(btn2x2)

        btn3x3 = QPushButton('3x3', self)
        btn3x3.clicked.connect(lambda: self.change_selection('3x3'))
        self.style_button(btn3x3)

        btn4x4 = QPushButton('4x4', self)
        btn4x4.clicked.connect(lambda: self.change_selection('4x4'))
        self.style_button(btn4x4)

        # Set up the layout
        layout = QVBoxLayout(self)
        layout.addWidget(label, alignment=Qt.AlignCenter)
        layout.addWidget(hint_label, alignment=Qt.AlignCenter)
        layout.addWidget(btn2x2)
        layout.addWidget(btn3x3)
        layout.addWidget(btn4x4)

        self.setLayout(layout)

    def style_label(self, label):
        label.setStyleSheet("font-size: 20px; margin-bottom: 10px; color: #333;")

    def style_hint_label(self, hint_label):
        hint_label.setStyleSheet("font-size: 14px; color: #777; margin-bottom: 20px;")

    def style_button(self, button):
        button.setStyleSheet(
            "font-size: 16px; padding: 15px; margin: 10px; background-color: #3498db; color: white; border: 2px solid #2980b9; border-radius: 8px;")

    def select_grid(self):
        if self.selection:
            self.show_dialog(int(self.selection[0]))

    def change_selection(self, selection):
        self.selection = selection
        self.select_grid()

    def show_dialog(self, n):
        dialog = QMessageBox(self)
        dialog.setWindowTitle("Grid Selected")
        dialog.setText(f"{n}x{n} grid selected")
        dialog.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GridSelector()
    window.show()
    sys.exit(app.exec_())