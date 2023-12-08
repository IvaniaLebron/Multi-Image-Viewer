import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class ImageGridApp(QWidget):
    #This is our constructor, recieves the paths of seleccted images, and the selected grid layout
    def __init__(self, image_paths, rows, cols):
        super().__init__()

        self.image_paths = image_paths
        self.rows = rows
        self.cols = cols

        self.images = []
        for path in self.image_paths:
            pixmap = QPixmap(path)
            self.images.append(pixmap)

        self.initUI()

    def initUI(self):
        grid_layout = QGridLayout()
        self.setLayout(grid_layout)

        # Calculate number of cells in the grid
        num_cells = self.rows * self.cols

        for i in range(num_cells):
            row = i // self.cols
            col = i % self.cols

            label = QLabel(self)
            label.setPixmap(self.images[i % len(self.images)])
            grid_layout.addWidget(label, row, col)

        self.setWindowTitle(f"Image Grid ({self.rows}x{self.cols})")
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Replace the image paths with your image paths
    image_paths = ['path_to_image1.jpg', 'path_to_image2.jpg', 'path_to_image3.jpg', 'path_to_image4.jpg']  # Add more paths as needed
    rows = 2  # You can change the number of rows
    cols = 2  # You can change the number of columns

    window = ImageGridApp(image_paths, rows, cols)
    sys.exit(app.exec_())
