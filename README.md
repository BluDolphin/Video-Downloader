# Video and Music Downloader
A simple program to automatically download Music, videos and playlists from a wide range of websites. 

When submitting a link you can choose to download the audio or video (w/audio). When downloading videos you can choose what resolution to download (NOTE - The program will try to download the highest resolution when the selected isn't avaliable)

IMPORTANT - When downloading videos it's best to install FFmpeg onto your device as the program primaraly uses it to add the audio to the downloaded videos. There is a fallback incase it is not installed, however this is significantly slower especially when downloading bulk/long videos.


#Screenshot
![Screenshot 2024-10-30 162854](https://github.com/user-attachments/assets/81d4196c-62f7-47a2-80cb-25bd4b33a61d) 
![Screenshot 2024-10-30 162927](https://github.com/user-attachments/assets/1cf57192-5119-4f4e-8ba4-35bccf2b11d1)


# Dependencies
To use the source code for the GUI program, the packages "yt_dlp", "pillow", "flet", "moviepy", and "bs4" will need to be installed via pip.

This can be done by using `pip install yt_dlp pillow flet moviepy bs4` in the terminal.
The "flet" package also requires additional dependancys for Linux, these can be found on their website [here](https://flet.dev/docs/publish/linux#prerequisites)

Downloading videos will be slower if ffmpeg is not installed, however you can still download videos without it.
to install ffmpeg you can run `pip install ffmpeg-python` or by installing it from the official website.


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

If ffmpeg is not installed then the program will automatically run in an alt mode where it will attempt to download the audio and video an merge them with moviepy. 
This allows for videos to be downloaded without ffmpeg at the cost of some speed.
