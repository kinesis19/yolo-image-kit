import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog, QTextEdit, QFormLayout
)
from PySide6.QtCore import QThread, Signal
from .processing import process_images


class Worker(QThread):
    progress = Signal(str)
    finished = Signal()

    def __init__(self, input_dir, output_dir, size, prefix):
        super().__init__()
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.size = size
        self.prefix = prefix

    def run(self):
        for message in process_images(self.input_dir, self.output_dir, self.size, self.prefix):
            self.progress.emit(message)
        self.finished.emit()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YOLO Image Kit")
        self.setGeometry(200, 200, 500, 400)
        self.initUI()

    def initUI(self):
        self.input_label = QLabel("Input folder:")
        self.input_path_edit = QLineEdit()
        self.input_btn = QPushButton("Select folder:")

        self.output_label = QLabel("Output folder:")
        self.output_path_edit = QLineEdit()
        self.output_btn = QPushButton("Select folder:")

        self.width_edit = QLineEdit("1280")
        self.height_edit = QLineEdit("720")
        self.prefix_edit = QLineEdit("image")

        self.start_btn = QPushButton("Start conversion")
        self.status_box = QTextEdit()
        self.status_box.setReadOnly(True)

        # Layout setting
        vbox = QVBoxLayout()

        # Select input/output folder
        input_hbox =QHBoxLayout()
        input_hbox.addWidget(self.input_path_edit)
        input_hbox.addWidget(self.input_btn)

        output_hbox =QHBoxLayout()
        output_hbox.addWidget(self.output_path_edit)
        output_hbox.addWidget(self.output_btn)

        # Form Layout
        form_layout = QFormLayout()
        form_layout.addRow(self.input_label, input_hbox)
        form_layout.addRow(self.output_label, output_hbox)
        size_layout = QHBoxLayout()
        size_layout.addWidget(self.width_edit)
        size_layout.addWidget(QLabel("x"))
        size_layout.addWidget(self.height_edit)
        form_layout.addRow("Image size (Horizontal x Vertical): ", size_layout)
        form_layout.addRow("File name prefix: ", self.prefix_edit)

        vbox.addLayout(form_layout)
        vbox.addWidget(self.start_btn)
        vbox.addWidget(QLabel("progress: "))
        vbox.addWidget(self.status_box)

        self.setLayout(vbox)

        # Connect signal and slot
        self.input_btn.clicked.connect(self.select_input_folder)
        self.output_btn.clicked.connect(self.select_output_folder)
        self.start_btn.clicked.connect(self.start_processing)

    def select_input_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select input folder")
        if folder_path:
            self.input_path_edit.setText(folder_path)

    def select_output_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select output folder")
        if folder_path:
            self.output_path_edit.setText(folder_path)

    def start_processing(self):
        input_dir = self.input_path_edit.text()
        output_dir = self.output_path_edit.text()
        prefix = self.prefix_edit.text()

        if not all ([input_dir, output_dir, prefix]):
            self.status_box.append("Error: Fill in all the fields")
            return
        
        try:
            width = int(self.width_edit.text())
            height = int(self.height_edit.text())
            size = (width, height)
        except ValueError:
            self.status_box.append("Error: Image size must be entered as a number")
            return

        self.start_btn.setEnabled(False)
        self.status_box.clear()
        self.status_box.append("Start image process...")

        # Start Thread
        self.worker = Worker(input_dir, output_dir, size, prefix)
        self.worker.progress.connect(self.update_status)
        self.worker.finished.connect(self.processing_finished)
        self.worker.start()

    def update_status(self, message):
        self.status_box.append(message)

    def processing_finished(self):
        self.start_btn.setEnabled(True)
        QApplication.beep()