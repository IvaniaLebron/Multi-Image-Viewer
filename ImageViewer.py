import sys
from PyQt5.QtWidgets import QApplication, QLabel,  QPushButton, QListWidget, QWidget, QMessageBox,QHBoxLayout, QVBoxLayout, QSplitter, QScrollArea
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QSize, Qt

class ImageViewer(QWidget):
  def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle(f'Image Viewer')
        self.setGeometry(100, 100, 600, 300)
        self.style_window(self)

        # Create widgets
        show_image = QLabel(self)
        show_image.setAlignment(Qt.AlignCenter)
        self.style_image(show_image)

        btn_previous_image = QPushButton('<', self)
        self.style_button(btn_previous_image)
        btn_previous_image.setFixedSize(75, 200)

        btn_next_image = QPushButton('>', self)
        self.style_button(btn_next_image)
        btn_next_image.setFixedSize(75,200)

        layout = QHBoxLayout(self)
        layout.addWidget(btn_previous_image)
        layout.addWidget(show_image)
        layout.addWidget(btn_next_image)

        

  def style_window(self, window):
       window.setStyleSheet("background-color: #343536;")

  def style_image(self, label):
        label.setStyleSheet("QLabel { background-color: grey; border-radius: 10px; }")

  def style_button(self, button):
        button.setStyleSheet("font-size: 25px; font-weight: bold; padding: 15px; margin: 10px; background-color:grey ; color: black; border: 2px solid grey; border-radius: 8px;")

  
       
  
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageViewer()
    window.show()
    sys.exit(app.exec_())