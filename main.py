import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QComboBox
from pytube import YouTube
from moviepy.editor import *

class YouTubeDownloader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Sampler")
        self.setGeometry(100, 100, 400, 200)

        self.url_label = QLabel("Enter YouTube Video URL:")
        self.url_input = QLineEdit()

        self.format_label = QLabel("Select File Format:")
        self.format_combobox = QComboBox()
        self.format_combobox.addItem("MP4")
        self.format_combobox.addItem("MP3")

        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.download_video)

        layout = QVBoxLayout()
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)
        layout.addWidget(self.format_label)
        layout.addWidget(self.format_combobox)
        layout.addWidget(self.download_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def download_video(self):
        url = self.url_input.text()
        file_format = self.format_combobox.currentText().lower()

        yt = YouTube(url)
        video = yt.streams.filter(file_extension=file_format).first()

        if video:
            video.download()
            print("Video downloaded successfully!")

            if file_format == 'mp3':
                video_file = '{}.mp4'.format(yt.title.replace(' ', '_'))
                convert_to_mp3(video_file)
        else:
            print("No {} stream found for the provided URL.".format(file_format.upper()))

def convert_to_mp3(video_file):
    video = VideoFileClip(video_file)
    mp3_file = video_file.replace(".mp4", ".mp3")
    video.audio.write_audiofile(mp3_file)
    print("Video converted to MP3 successfully!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = YouTubeDownloader()
    window.show()
    sys.exit(app.exec())

