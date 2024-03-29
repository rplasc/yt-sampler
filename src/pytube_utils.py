import os
import subprocess
import re
from pytube import YouTube

def load_streams(main_window):
    url = main_window.url_input.text()  # Get the URL from the input field
    yt = None  # Create a YouTube object
            
    try:
        yt = YouTube(url)
        
        # Remove invalid characters and display title on main window
        invalid_chars = r'[<>:"/\\|?*]'
        main_window.video_title = re.sub(invalid_chars, '', yt.title)
        main_window.video_title_text.setText(main_window.video_title)

        try:
            main_window.streams = yt.streams.filter(adaptive=True)
            main_window.enable_widgets()        
            # Clear existing items in the combo boxes
            main_window.resolution_combobox.clear()
            main_window.abr_combobox.clear()
            
            # Populate the resolution and audio bitrate combo boxes
            for stream in main_window.streams:
                if stream.mime_type.startswith('audio'):
                    main_window.abr_combobox.addItem(stream.abr)
                elif stream.mime_type.startswith('video'):
                    main_window.resolution_combobox.addItem(stream.resolution)
        except Exception as e:
            main_window.show_message("Error", "No stream found for the provided URL.")
    except Exception as e:
        main_window.show_message("Error", "Please enter a valid URL.")

def download_stream(main_window):
    # Get the selected resolution and audio bitrate
    resolution = main_window.resolution_combobox.currentText()
    abr = main_window.abr_combobox.currentText()
    audio_only = main_window.audio_only_checkbox.isChecked()
    mp3 = main_window.mp3_checkbox.isChecked()
    
    # Get the selected streams
    video_stream = None
    audio_stream = None
    
    for stream in main_window.streams:
        if stream.resolution == resolution:
            video_stream = stream
        elif stream.abr == abr and stream.mime_type.startswith('audio'):
            audio_stream = stream
            
        if video_stream and audio_stream:
            break

    if not audio_only and video_stream is None:
        main_window.show_message("Error", "Video stream not found.")
        return
    elif audio_only and audio_stream is None:
        main_window.show_message("Error", "Audio stream not found.")
        return

    # Download the selected streams
    try:
        if audio_only:
            # Download only audio stream
            if main_window.mp3_checkbox.isChecked():
                audio_stream.download(filename=f"{main_window.video_title}.mp3", output_path=main_window.download_location)
                main_window.show_message("Download Successful", "Audio downloaded as mp3.")
            else:
                audio_stream.download(filename=f"{main_window.video_title}.wav", output_path=main_window.download_location)
                main_window.show_message("Download Successful", "Audio downloaded as WAV.")

        else:
            # Download video stream
            video_stream.download(output_path=main_window.download_location, filename=f"{main_window.video_title}_video")
            audio_stream.download(output_path=main_window.download_location, filename=f"{main_window.video_title}_audio")

            # Create paths to files
            video_path = f"{main_window.download_location}/{main_window.video_title}_video"
            audio_path = f"{main_window.download_location}/{main_window.video_title}_audio"

            # Merge video and audio using ffmpeg
            merged_path = f"{main_window.download_location}/{main_window.video_title}.mp4"
            subprocess.run(["ffmpeg", "-i", video_path, "-i", audio_path, "-c:v", "copy", "-c:a", "aac", merged_path], capture_output=True)
        
            # Remove the original video and audio files
            os.remove(video_path)
            os.remove(audio_path)
        
            main_window.show_message("Info", "Video downloaded.")
    except Exception as e:
        main_window.show_message("Error", f"Error downloading stream: {str(e)}")