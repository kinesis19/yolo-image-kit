import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog, QTextEdit, QFormLayout, QTabWidget
)
from PySide6.QtCore import QThread, Signal
from .processing import process_images, extract_frames_from_video


class ImageWorker(QThread):
    progress = Signal(str)
    finished = Signal(object)

    def __init__(self, input_dir, output_dir, size, prefix):
        super().__init__()
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.size = size
        self.prefix = prefix

    def run(self):
        for message in process_images(self.input_dir, self.output_dir, self.size, self.prefix):
            self.progress.emit(message)
        self.finished.emit(None)

class VideoWorker(QThread):
    progress = Signal(str)
    finished = Signal(object)

    def __init__(self, video_path, output_dir, prefix):
        super().__init__()
        self.video_path = video_path
        self.output_dir = output_dir
        self.prefix = prefix

    def run(self):
        for message in extract_frames_from_video(self.video_path, self.output_dir, self.prefix):
            self.progress.emit(message)
        self.finished.emit(None)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YOLO Image Kit")
        self.setGeometry(200, 200, 500, 400)
        self.initUI()

    def initUI(self):

        # Main layout
        main_layout = QVBoxLayout(self)

        # Tab Widget
        tabs = QTabWidget()

        self.image_tab = self.create_image_processing_tab()
        self.video_tab = self.create_video_extraction_tab()

        # Add tab
        tabs.addTab(self.image_tab, "Image Resizing")
        tabs.addTab(self.video_tab, "Video to Frames")

        main_layout.addWidget(tabs)
        self.setLayout(main_layout)

    def create_image_processing_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        form_layout = QFormLayout()

        self.img_input_path_edit = QLineEdit()
        self.img_input_btn = QPushButton("Select folder:")
        input_hbox = QHBoxLayout()
        input_hbox.addWidget(self.img_input_path_edit)
        input_hbox.addWidget(self.img_input_btn)
        
        self.img_output_path_edit = QLineEdit()
        self.img_output_btn = QPushButton("Select folder:")
        output_hbox = QHBoxLayout()
        output_hbox.addWidget(self.img_output_path_edit)
        output_hbox.addWidget(self.img_output_btn)

        form_layout.addRow("Input Folder:", input_hbox)
        form_layout.addRow("Output Folder:", output_hbox)

        size_layout = QHBoxLayout()
        self.img_width_edit = QLineEdit("800")
        self.img_height_edit = QLineEdit("600")
        size_layout.addWidget(self.img_width_edit)
        size_layout.addWidget(QLabel("x"))
        size_layout.addWidget(self.img_height_edit)
        form_layout.addRow("Image Size (Width x Height): ", size_layout)

        self.img_prefix_edit = QLineEdit("image")
        form_layout.addRow("File Name Prefix: ", self.img_prefix_edit)

        self.img_start_btn = QPushButton("Start conversion")
        self.img_status_box = QTextEdit()
        self.img_status_box.setReadOnly(True)

        layout.addLayout(form_layout)
        layout.addWidget(self.img_start_btn)
        layout.addWidget(QLabel("Progress: "))
        layout.addWidget(self.img_status_box)

        # Connect Signal-slot 
        self.img_input_btn.clicked.connect(lambda: self.select_folder(self.img_input_path_edit))
        self.img_output_btn.clicked.connect(lambda: self.select_folder(self.img_output_path_edit))
        self.img_start_btn.clicked.connect(self.start_image_processing)

        return tab

    def create_video_extraction_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        form_layout = QFormLayout()

        self.vid_input_path_edit = QLineEdit()
        self.vid_input_btn = QPushButton("Select Video File")
        input_hbox = QHBoxLayout()
        input_hbox.addWidget(self.vid_input_path_edit)
        input_hbox.addWidget(self.vid_input_btn)

        self.vid_output_path_edit = QLineEdit()
        self.vid_output_btn = QPushButton("Select Folder")
        output_hbox = QHBoxLayout()
        output_hbox.addWidget(self.vid_output_path_edit)
        output_hbox.addWidget(self.vid_output_btn)

        self.vid_prefix_edit = QLineEdit("frame")

        form_layout.addRow("Video File:", input_hbox)
        form_layout.addRow("Output Folder:", output_hbox)
        form_layout.addRow("Frame Name Prefix:", self.vid_prefix_edit)

        self.vid_start_btn = QPushButton("Start Extraction")
        self.vid_status_box = QTextEdit()
        self.vid_status_box.setReadOnly(True)

        layout.addLayout(form_layout)
        layout.addWidget(self.vid_start_btn)
        layout.addWidget(QLabel("Progress:"))
        layout.addWidget(self.vid_status_box)

        # Connect Signal-Slog
        self.vid_input_btn.clicked.connect(self.select_video_file)
        self.vid_output_btn.clicked.connect(lambda: self.select_folder(self.vid_output_path_edit))
        self.vid_start_btn.clicked.connect(self.start_video_extraction)

        return tab


    def select_folder(self, line_edit):
        folder_path = QFileDialog.getExistingDirectory(self, "Select folder")
        if folder_path:
            line_edit.setText(folder_path)

    def select_video_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Video File", "", "Video Files (*.mp4 *.avi *.mov *.mkv)")
        if file_path:
            self.vid_input_path_edit.setText(file_path)
    
    
    def start_image_processing(self):
        input_dir = self.img_input_path_edit.text()
        output_dir = self.img_output_path_edit.text()
        prefix = self.img_prefix_edit.text()

        if not all ([input_dir, output_dir, prefix]):
            self.update_status("Error: File in all the fields.", self.img_status_box)
            return
        try:
            size = (int(self.img_width_edit.text()), int(self.img_height_edit.text()))
        except ValueError:
            self.update_status("Error: Image size must be a number.", self.img_status_box)
            return

        self.img_start_btn.setEnabled(False)
        self.img_status_box.clear()
        self.update_status("Starting image processing...", self.img_status_box)

        # Start Thread
        self.worker = ImageWorker(input_dir, output_dir, size, prefix)
        self.worker.progress.connect(lambda msg: self.update_status(msg, self.img_status_box))
        self.worker.finished.connect(lambda: self.processing_finished(self.img_start_btn))
        self.worker.start()

    def start_video_extraction(self):
        video_path = self.vid_input_path_edit.text()
        output_dir = self.vid_output_path_edit.text()
        prefix = self.vid_prefix_edit.text()

        if not all([video_path, output_dir, prefix]):
            self.update_status("Error: Fill in all the fields.", self.vid_status_box)
            return
        
        self.vid_start_btn.setEnabled(False)
        self.vid_status_box.clear()
        self.update_status("Starting video frame extraction...", self.vid_status_box)

        self.video_worker = VideoWorker(video_path, output_dir, prefix)
        self.video_worker.progress.connect(lambda msg: self.update_status(msg, self.vid_status_box))
        self.video_worker.finished.connect(lambda: self.processing_finished(self.vid_start_btn))
        self.video_worker.start()

    def update_status(self, message, status_box):
        status_box.append(message)

    def processing_finished(self, button_to_enable):
        button_to_enable.setEnabled(True)
        QApplication.beep()