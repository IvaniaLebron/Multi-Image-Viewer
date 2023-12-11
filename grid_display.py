import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QWidget, QVBoxLayout, QScrollArea, QGridLayout
from PyQt5.QtGui import QPixmap, QImage, QPainter
from PyQt5.QtCore import Qt, pyqtSignal
import cv2

class ZoomableGraphicsView(QGraphicsView):
    zoomChanged = pyqtSignal(float)

    def __init__(self, scene, parent=None):
        super(ZoomableGraphicsView, self).__init__(scene, parent)
        self.setRenderHint(QPainter.Antialiasing, True)
        self.setRenderHint(QPainter.SmoothPixmapTransform, True)
        self.setRenderHint(QPainter.HighQualityAntialiasing, True)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.global_zoom_factor = 1.0  # Initialize the global zoom factor

    def wheelEvent(self, event):
        factor = 1.2
        if event.angleDelta().y() < 0:
            factor = 1.0 / factor

        # Get the position of the mouse cursor in the scene
        mouse_scene_pos = self.mapToScene(event.pos())

        # Apply the zoom centered around the mouse cursor
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setTransform(self.transform().translate(mouse_scene_pos.x(), mouse_scene_pos.y()).scale(factor, factor).translate(-mouse_scene_pos.x(), -mouse_scene_pos.y()))

        self.global_zoom_factor = self.transform().m11()
        self.zoomChanged.emit(self.global_zoom_factor)

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
        self.views = []

        for row in range(self.rows):
            for col in range(self.cols):
                index = row * self.cols + col
                if index < len(self.image_paths):
                    image_path = self.image_paths[index]
                    pixmap = self.load_image(image_path)

                    scene = QGraphicsScene(self)
                    item = QGraphicsPixmapItem(pixmap)
                    scene.addItem(item)

                    view = ZoomableGraphicsView(scene, self)
                    view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                    view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                    grid_layout.addWidget(view, row, col)

                    view.zoomChanged.connect(self.handleZoomChange)
                    self.views.append(view)

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

    def handleZoomChange(self, zoom_factor):
        for view in self.views:
            if view.global_zoom_factor != zoom_factor:
                view.setTransform(view.transform().scale(zoom_factor, zoom_factor))
                view.global_zoom_factor = zoom_factor

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        image_paths = ['path_to_image1.jpg', 'path_to_image2.jpg', 'path_to_image3.jpg', 'path_to_image4.jpg']
        rows = 2
        cols = 2

        window = GridDisplayApp(image_paths, rows, cols)
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Error in main block: {str(e)}")
