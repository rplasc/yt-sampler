import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QFileDialog, QMessageBox, QCheckBox
from pytube import YouTube
from moviepy.editor import *

class Sampler(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Downloader")  # Set the window title
        self.setGeometry(100, 100, 400, 250)  # Set the window size and position

        # Create UI elements
        self.url_label = QLabel("Enter YouTube Video URL:")
        self.url_input = QLineEdit()

        self.location_label = QLabel("Download Location:")
        self.location_input = QLineEdit()
        self.location_input.setReadOnly(True)

        self.convert_checkbox = QCheckBox("Convert to MP3")
        self.convert_checkbox.clicked.connect(self.convert_to_mp3)

        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.download_video)

        # Create a layout and add UI elements to it
        layout = QVBoxLayout()
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)
        layout.addWidget(self.location_label)
        layout.addWidget(self.location_input)
        layout.addWidget(self.convert_checkbox)
        layout.addWidget(self.download_button)

        # Set the layout for the central widget
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.download_location = None  # Variable to store the download location

    def choose_location(self):
        self.download_location = QFileDialog.getExistingDirectory(self, "Choose Download Location")
        if self.download_location:
            self.location_input.setText(self.download_location)

    def download_video(self):
        url = self.url_input.text()  # Get the URL from the input field
        yt = YouTube(url)  # Create a YouTube object
        video = yt.streams.first()  # Get the first stream

        if video:  # Check if a stream was found
            try:
                if not self.download_location:
                    self.choose_location()  # If download location is not set, prompt the user to choose a location

                if self.download_location:
                    video.download(output_path=self.download_location)  # Download the video to the selected location
                else:
                    self.show_message("Error", "Download location not set.")
                    return

                self.show_message("Success", "Video downloaded successfully!")

            except Exception as e:
                self.show_message("Error", str(e))
        else:
            self.show_message("Error", "No stream found for the provided URL.")

    def convert_to_mp3(self):
        if self.convert_checkbox.isChecked():
            video_file = QFileDialog.getOpenFileName(self, "Choose Video File", filter="Video Files (*.mp4 *.avi *.mkv)")[0]
            if video_file:
                video = VideoFileClip(video_file)  # Load the video file
                mp3_file = video_file.replace(".mp4", ".mp3")  # Replace the file extension
                video.audio.write_audiofile(mp3_file)  # Write the audio to a new file
                print("Video converted to MP3 successfully!")
            else:
                self.convert_checkbox.setChecked(False)

    def show_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Sampler()
    window.show()
    sys.exit(app.exec())
