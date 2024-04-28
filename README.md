# YouTube Downloader
A very simple program to automatically download videos and playlists from youtube.

The program is console based (currently), and allows for downloading both audio and videos in multiple fomats

# Dependencies
To run the program you will need to have "ffmpeg" installed on your system, regardless if your using the source code or the exe.

This can be done from the offical website at https://ffmpeg.org/download.html

To use the source code then you will need to download "yt_dlp" and "FFmpeg-python" packages via pip.

This can be done by using the `pip install yt_dlp ffmpeg-python` command in the terminal.

## Info
The video/playlist needs to be either public or unlisted, otherwise the program will not be able to retrieve the it from YT.

After entering the URL you can chose to download the video(w/ audio) or only audio. Which are downloaded in mp4 and m4a respectively.

downloaded videos have their names copied from youtube and are saved in a new folder called downloads in the current directory.
