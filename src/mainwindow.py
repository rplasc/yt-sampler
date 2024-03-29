from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QFileDialog, QMessageBox, QCheckBox, QComboBox
from src.pytube_utils import load_streams, download_stream

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Downloader")
        self.setGeometry(100, 100, 400, 250)  # Set the window size and position
        
        self.url_label = QLabel("Enter YouTube Video URL:")
        self.url_input = QLineEdit()
        
        self.load_button = QPushButton("Load")
        self.load_button.clicked.connect(lambda: load_streams(self))
        
        self.video_title_text = QLabel("No Video Loaded")
        
        self.resolution_label = QLabel("Available Resolutions:")
        self.resolution_combobox = QComboBox()
        
        self.abr_label = QLabel("Available Audio Bitrates:")
        self.abr_combobox = QComboBox()
        
        self.location_label = QLabel("Download Location:")
        self.location_text = QLabel("Not Set")
        self.location_button = QPushButton("Set Location")
        self.location_button.clicked.connect(self.choose_location)
        
        self.audio_only_checkbox = QCheckBox("Audio Only")
        self.audio_only_checkbox.stateChanged.connect(self.toggle_mp3_checkbox)
        
        self.mp3_checkbox = QCheckBox("Download as .mp3 (Default is .wav)")
        
        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(lambda: download_stream(self))
        
        # Disable all widgets initially
        self.disable_widgets()

        # Create layout
        layout = QVBoxLayout()
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)
        layout.addWidget(self.load_button)
        layout.addWidget(self.video_title_text)
        layout.addWidget(self.resolution_label)
        layout.addWidget(self.resolution_combobox)
        layout.addWidget(self.abr_label)
        layout.addWidget(self.abr_combobox)
        layout.addWidget(self.location_label)
        layout.addWidget(self.location_text)
        layout.addWidget(self.location_button)
        layout.addWidget(self.audio_only_checkbox)
        layout.addWidget(self.mp3_checkbox)
        layout.addWidget(self.download_button)

        # Set the layout for the central widget
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        
        self.download_location = None  # Variable to store the download location
        #self.downloaded_resolution = None  # Variable to store the resolution of the downloaded video
        self.streams = [] # List to hold found streams
        self.video_title = None # Variable to store the title of the video

    def show_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()
        
    def choose_location(self):
        self.download_location = QFileDialog.getExistingDirectory(self, "Choose Download Location")
        if self.download_location:
            self.location_text.setText(self.download_location)
            self.download_button.setEnabled(True)
            
    def disable_widgets(self):
        self.resolution_combobox.setEnabled(False)
        self.abr_combobox.setEnabled(False)
        self.location_button.setEnabled(False)
        self.audio_only_checkbox.setEnabled(False)
        self.mp3_checkbox.setEnabled(False)
        self.download_button.setEnabled(False)

    def enable_widgets(self):
        self.resolution_combobox.setEnabled(True)
        self.abr_combobox.setEnabled(True)
        self.location_button.setEnabled(True)
        self.audio_only_checkbox.setEnabled(True)
        
    def toggle_mp3_checkbox(self, state):
        if state == Qt.CheckState.Checked:
            self.mp3_checkbox.setEnabled(True)
        else:
            self.mp3_checkbox.setEnabled(False)
            self.mp3_checkbox.setChecked(False)