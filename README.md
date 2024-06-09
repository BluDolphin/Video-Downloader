# Video and Music Downloader
A very simple program to automatically download Music, videos and playlists from a wide range of websites.

# Dependencies
## GUI
To use the source code for the GUI program, the packages "yt_dlp", "pillow" and "flet" will need to be installed via pip
This can be done by using `pip install yt_dlp pillow flet` in the terminal.

## CLI
To use the source code both "yt_dlp" and "FFmpeg-python" packages will need to be installed via pip.
This can be done by using `pip install yt_dlp ffmpeg-python` in the terminal.

# Info
To be able to download the media will need to be public.
For example on youtube the it needs to be either public or unlisted, otherwise the program will not be able to retrieve it.

After entering the URL you can chose to download the video(w/ audio) or only audio. Which are downloaded in mp4 and m4a respectively.

downloaded videos have their names copied from the source and are saved in a new folder called downloads in the current directory.

As well as this thumbnails for the media are stored in a temp folder in "downloads/temp/". When the program runs it will automatically fush this.
