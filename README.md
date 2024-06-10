# Video and Music Downloader
A very simple program to automatically download Music, videos and playlists from a wide range of websites.

# Dependencies
To use the source code for the GUI program, the packages "yt_dlp", "pillow", "flet", and "bs4" will need to be installed via pip.

This can be done by using `pip install yt_dlp pillow flet bs4` in the terminal.

To download videos ffmpeg will need to be downloaded.
This can be done by running `pip install ffmpeg-python` or by installing it from the official website.


## Legacy program (CLI)
The `yt-dlp` python package will need to be install via pip to use.
To use custom formats or to download videos then ffmpeg will also need to be installed.
This can be done by using `pip install yt_dlp ffmpeg-python` in the terminal.

# Info
To be able to download the media will need to be public.
For example on youtube the it needs to be either public or unlisted, otherwise the program will not be able to retrieve it.

After entering the URL you can chose to download the video(w/ audio) or only audio. Which are downloaded in mp4 and m4a respectively.

Downloaded videos have their names copied from the source and are saved in a new folder called downloads in the current directory.

As well as this thumbnails for the media are stored in a temp folder in "downloads/temp/". When the program runs it will automatically flush all previously downloaded thumbnails.
