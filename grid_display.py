import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QWidget, QVBoxLayout, QScrollArea, QGridLayout
from PyQt5.QtGui import QPixmap, QImage, QPainter
from PyQt5.QtCore import Qt
import cv2

class ZoomableGraphicsView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super(ZoomableGraphicsView, self).__init__(scene, parent)
        self.setRenderHint(QPainter.Antialiasing, True)
        self.setRenderHint(QPainter.SmoothPixmapTransform, True)
        self.setRenderHint(QPainter.HighQualityAntialiasing, True)

    def wheelEvent(self, event):
        factor = 1.2
        if event.angleDelta().y() < 0:
            factor = 1.0 / factor

        self.scale(factor, factor)

class GridDisplayApp(QWidget):
    def __init__(self, image_paths, rows, cols):
        super().__init__()

        self.image_paths = image_paths
        self.rows = rows
        self.cols = cols

        self.setWindowTitle('Image Grid Display')
        self.setGeometry(100, 100, 800, 600)

        self.initUI()

    def initUI(self):
        grid_layout = QGridLayout(self)

        for row in range(self.rows):
            for col in range(self.cols):
                index = row * self.cols + col
                if index < len(self.image_paths):
                    image_path = self.image_paths[index]
                    pixmap = self.load_image(image_path)

                    scene = QGraphicsScene(self)  # Create a new scene for each image
                    item = QGraphicsPixmapItem(pixmap)
                    scene.addItem(item)

                    view = ZoomableGraphicsView(scene, self)
                    view.setSceneRect(scene.sceneRect())
                    view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                    view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

                    grid_layout.addWidget(view, row, col)

        widget = QWidget(self)
        widget.setLayout(grid_layout)

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(widget)

        layout = QVBoxLayout(self)
        layout.addWidget(scroll_area)

        self.setLayout(layout)

    def load_image(self, path):
        img = cv2.imread(path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        height, width, channel = img.shape
        bytes_per_line = 3 * width
        qimg = QImage(img_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        return pixmap

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        image_paths = ['path_to_image1.jpg', 'path_to_image2.jpg', 'path_to_image3.jpg', 'path_to_image4.jpg']  # Add more paths as needed
        rows = 2
        cols = 2

        window = GridDisplayApp(image_paths, rows, cols)
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Error: {str(e)}")
