import sys
from PySide6.QtWidgets import QApplication
from yolo_kit.main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())