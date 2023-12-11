import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QVBoxLayout
from PyQt5.QtGui import QImage, QPixmap, QPainter, QTransform, QColor  
from PyQt5.QtWidgets import QRubberBand 
from PyQt5.QtCore import Qt, QRectF, QRect



class ZoomableGraphicsView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.setRenderHint(QPainter.Antialiasing, True)
        self.setRenderHint(QPainter.SmoothPixmapTransform, True)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setRenderHint(QPainter.Antialiasing, True)
        self.setRenderHint(QPainter.SmoothPixmapTransform, True)
        self.setRenderHint(QPainter.HighQualityAntialiasing, True)
        self.setRenderHint(QPainter.TextAntialiasing, True)

    def wheelEvent(self, event):
        factor = 1.2
        if event.angleDelta().y() < 0:
            factor = 1.0 / factor
        self.scale(factor, factor)

class ImageGridApp(QGraphicsView):
    def __init__(self, image_paths, rows, cols):
        super().__init__()

        self.rows = rows
        self.cols = cols

        # Create a QGraphicsScene
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        # Calculate cell size
        cell_width = 400 // cols
        cell_height = 300 // rows

        for i, path in enumerate(image_paths):
            row = i // cols
            col = i % cols

            # Load the image as QImage
            image = QImage(path)

            # Create a QGraphicsPixmapItem for each image
            pixmap_item = QGraphicsPixmapItem(QPixmap.fromImage(image))
            pixmap_item.setTransformationMode(Qt.SmoothTransformation)  # Preserve image quality
            pixmap_item.setPos(col * cell_width, row * cell_height)

            # Add the item to the scene
            self.scene.addItem(pixmap_item)

        # Set up the view
        self.setFixedSize(400, 300)
        self.setSceneRect(0, 0, 400, 300)

        # Create a zoomable view
        self.zoomable_view = ZoomableGraphicsView(self.scene)

        # Set up the layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.zoomable_view)

        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    image_paths = ['path_to_image1.jpg', 'path_to_image2.jpg', 'path_to_image3.jpg', 'path_to_image4.jpg']  # Add more paths as needed
    rows = 2
    cols = 2

    window = ImageGridApp(image_paths, rows, cols)
    window.show()
    sys.exit(app.exec_())






