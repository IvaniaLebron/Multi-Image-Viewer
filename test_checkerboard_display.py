import sys
import unittest
from unittest.mock import patch  
from PyQt5.QtWidgets import QApplication
from checkerboard_display import CheckerboardDisplayApp
from PyQt5.QtGui import QPixmap

# Initialize QApplication
app = QApplication(sys.argv)

class TestCheckerboardDisplayApp(unittest.TestCase):

    def setUp(self):
        # Create mock images with specific sizes
        self.mock_image1 = QPixmap(100, 100)
        self.mock_image2 = QPixmap(150, 150)
        self.app = CheckerboardDisplayApp(self.mock_image1, self.mock_image2, 10)
       
    def test_checkerboard_dimensions(self):
        # Verify if the width and height of the board are as expected
        expected_width = max(self.mock_image1.width(), self.mock_image2.width())
        expected_height = max(self.mock_image1.height(), self.mock_image2.height())
        
        self.assertEqual(self.app.checkerboard_width, expected_width)
        self.assertEqual(self.app.checkerboard_height, expected_height)

    def test_checkerboard_pixmap_creation(self):
        # Verify if the QPixmap of the checkerboard has been created
        self.assertIsNotNone(self.app.original_pixmap)

    def test_incorrect_number_of_images(self):
        # Create an instance with an incorrect number of images
        with self.assertRaises(ValueError):  
            CheckerboardDisplayApp('path_to_image1.jpg', None, 10)  # Only one image provided

        with self.assertRaises(ValueError):  
            CheckerboardDisplayApp(None, None, 10) # No image
            
    def test_invalid_square_size(self):
        # Create an instance with an invalid square size
        with self.assertRaises(ValueError):
            CheckerboardDisplayApp(self.mock_image1, self.mock_image2, -1)  # Negative square size

        with self.assertRaises(ValueError):
            CheckerboardDisplayApp(self.mock_image1, self.mock_image2, 0)  # Zero square size

        with self.assertRaises(ValueError):
            CheckerboardDisplayApp(self.mock_image1, self.mock_image2, "invalid")  # Non-integer square size

    @patch('PyQt5.QtWidgets.QFileDialog.getSaveFileName')
    @patch('PyQt5.QtGui.QPixmap.save')
    def test_save_image(self, mock_save, mock_get_save_file_name):
        
        mock_get_save_file_name.return_value = ('/path/to/save/image.jpg', '')

        # Call save_image
        self.app.save_image()

        # Verify that getSaveFileName was called
        mock_get_save_file_name.assert_called_once()

        # Verify that the save method was called with the correct path
        mock_save.assert_called_once_with('/path/to/save/image.jpg')

if __name__ == '__main__':
    unittest.main()
