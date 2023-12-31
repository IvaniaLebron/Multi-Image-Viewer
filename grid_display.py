import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QWidget, QVBoxLayout, QScrollArea, QGridLayout
from PyQt5.QtGui import QPixmap, QImage, QPainter
from PyQt5.QtCore import Qt, pyqtSignal
import cv2

class DraggableGraphicsPixmapItem(QGraphicsPixmapItem):
    def __init__(self, pixmap):
        super(DraggableGraphicsPixmapItem, self).__init__(pixmap)
        self.setFlag(QGraphicsPixmapItem.ItemIsMovable)

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
        self.setInteractive(True)  # Enable mouse events
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.drag_start_pos = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_pos = event.pos()
        elif event.button() == Qt.RightButton:
            # Zoom out on right-click
            self.zoom(1 / 1.5)

        super(ZoomableGraphicsView, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.drag_start_pos is not None:
            # Calculate the movement vector and apply it to all items in the scene
            delta = event.pos() - self.drag_start_pos
            for item in self.scene().items():
                if isinstance(item, DraggableGraphicsPixmapItem):
                    item.setPos(item.pos() + delta)

            self.drag_start_pos = event.pos()

        super(ZoomableGraphicsView, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_pos = None

        super(ZoomableGraphicsView, self).mouseReleaseEvent(event)

    def wheelEvent(self, event):
        # Disable the default wheel behavior to prevent unwanted scrolling
        factor = 1.2
        if event.angleDelta().y() < 0:
            factor = 1.0 / factor

        self.setTransform(self.transform().scale(factor, factor))
        self.global_zoom_factor = self.transform().m11()
        self.zoomChanged.emit(self.global_zoom_factor)

    def zoom(self, factor):
        self.setTransform(self.transform().scale(factor, factor))
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

        reference_view = None  # Store the reference view for zoom synchronization

        for row in range(self.rows):
            for col in range(self.cols):
                index = row * self.cols + col
                if index < len(self.image_paths):
                    image_path = self.image_paths[index]
                    pixmap = self.load_image(image_path)

                    scene = QGraphicsScene(self)
                    item = DraggableGraphicsPixmapItem(pixmap)  # Use the custom item for draggable behavior
                    scene.addItem(item)

                    view = ZoomableGraphicsView(scene, self)
                    grid_layout.addWidget(view, row, col)

                    view.zoomChanged.connect(self.handleZoomChange)
                    self.views.append(view)

                    if reference_view is None:
                        reference_view = view
                    else:
                        # Synchronize viewports
                        view.setSceneRect(reference_view.sceneRect())

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

        desired_height = self.size().height() / self.rows  # Get the height of the square
        scaled_width = int(width * (desired_height / height))

        # Creating QImage with specific interpolation method (Qt.AA_Scaled uses bilinear interpolation by default)
        qimg = QImage(img_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg).scaled(scaled_width, int(desired_height),
                                               aspectRatioMode=Qt.IgnoreAspectRatio,
                                               transformMode=Qt.FastTransformation)
        return pixmap

    def handleZoomChange(self, zoom_factor):
        for view in self.views:
            # Calculate the relative zoom factor based on the original zoom level
            relative_zoom = zoom_factor / view.global_zoom_factor
            view.setTransform(view.transform().scale(relative_zoom, relative_zoom))

            # Adjust the scene rect to update the zoom level for all views
            view.setSceneRect(self.views[0].sceneRect())
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
