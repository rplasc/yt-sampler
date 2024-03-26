import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QFileDialog, QMessageBox, QCheckBox, QComboBox
from pytube import YouTube
from moviepy.editor import *
import os

class Sampler(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Downloader")  # Set the window title
        self.setGeometry(100, 100, 400, 250)  # Set the window size and position

        # Create UI elements
        self.url_label = QLabel("Enter YouTube Video URL:")
        self.url_input = QLineEdit()

        self.location_label = QLabel("Download Location:")
        self.location_text = QLabel("Not set")


        self.convert_checkbox = QCheckBox("Convert to MP3")

        self.resolution_label = QLabel("Select Resolution:")
        self.resolution_combobox = QComboBox()
        self.resolution_combobox.addItems(["Default (720p)", "Highest", "Lowest"])

        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.download_video)

        # Create a layout and add UI elements to it
        layout = QVBoxLayout()
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)
        layout.addWidget(self.convert_checkbox)
        layout.addWidget(self.resolution_label)
        layout.addWidget(self.resolution_combobox)
        layout.addWidget(self.download_button)
        layout.addWidget(self.location_label)
        layout.addWidget(self.location_text)
        
        # Set the layout for the central widget
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.download_location = None  # Variable to store the download location
        self.downloaded_resolution = None  # Variable to store the resolution of the downloaded video

    def choose_location(self):
        self.download_location = QFileDialog.getExistingDirectory(self, "Choose Download Location")
        if self.download_location:
            self.location_text.setText(self.download_location)

    def download_video(self):
        try:
            url = self.url_input.text()  # Get the URL from the input field
            yt = YouTube(url)  # Create a YouTube object

            # Get the selected resolution
            selected_resolution = self.resolution_combobox.currentText()
            if selected_resolution == "Lowest":
                video = yt.streams.filter(progressive=True).order_by('resolution').first()
            elif selected_resolution == "Default (720p)":
                video = yt.streams.filter(res="720p").first()
            elif selected_resolution == "Highest":
                video = yt.streams.filter(progressive=True).order_by('resolution').desc().first()
            else:
                video = yt.streams.filter(progressive=True, resolution=selected_resolution[:-1]).first()

            if video:  # Check if a stream was found
                try:
                    if not self.download_location:
                        self.choose_location()  # If download location is not set, prompt the user to choose a location

                    if self.download_location:
                        video_path = video.download(output_path=self.download_location)  # Download the video to the selected location
                        while os.path.getsize(video_path) < video.filesize:
                            pass
                        
                        if self.convert_checkbox.isChecked():
                            self.convert_to_mp3(video_path)  # Convert the downloaded video to MP3
                            os.remove(video_path)  # Remove the MP4 version
                    else:
                        self.show_message("Error", "Download location not set.")
                        return

                    self.downloaded_resolution = video.resolution
                    self.show_message("Success", f"Video downloaded successfully!\nResolution: {self.downloaded_resolution}")

                except Exception as e:
                    self.show_message("Error", str(e))
            else:
                self.show_message("Error", "No stream found for the provided URL.")
        except Exception as e:
            self.show_message("Error", "The URL is invalid.")

    def convert_to_mp3(self, video_path):
        video = VideoFileClip(video_path)  # Load the video file
        mp3_file = video_path.replace(".mp4", ".mp3")  # Replace the file extension
        video.audio.write_audiofile(mp3_file)  # Write the audio to a new file
        video.close()  # Close the video file

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
