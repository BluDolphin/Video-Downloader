import yt_dlp

def audioOrVideo():
    print("\nWhich do you want to download:"
          "\n1) Audio"
          "\n2) Video")
    
    if (temp:=input("Input: ")) == "1":
        return "bestaudio[ext=mp4]/best" #Return True for audio
    elif temp == "2": 
        return "bestvideo[ext=mp4]/best" #Return False for video
    else:
        print("Invalid Input")
        audioOrVideo()

def my_hook(d):
    if d['status'] == 'finished':
        print("\nFinished downloading: ", d['filename'])

def Download():
    print("\n========= Youtube Downloader ========="
          "\nPlaylists need to be set to public or unlisted to be downloaded."
          "\nInput the URL of the playlist or single to download:")
    usrInput = input("\nURL: ")
    
    AorV = audioOrVideo()
    
    print("\nStarting download...")
    
    ydl_opts = {
    'noplaylist': False,  # Download just the video, if the URL refers to a video and a playlist.
    'quiet': True,  # Do not print messages to stdout.
    'format': AorV,  # Choice of quality.
    'outtmpl': 'downloads/%(title)s.%(ext)s',  # Name the file the ID of the video
    'restrictfilenames': True,  # Restrict filenames to only ASCII characters, and avoid "&" and spaces in filenames
    'nooverwrites': True,  # Prevent overwriting files.
    'continuedl': True,  # Force resume of partially downloaded files.
    'progress_hooks': [my_hook],  # Hook function that gets called before the download starts
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([usrInput])
    except:
        print("\nError: Invalid URL")
        Download()

Download()