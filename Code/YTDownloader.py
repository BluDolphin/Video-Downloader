import yt_dlp

def Download():
    print("\n========= Youtube Downloader ========="
          "\nPlaylists need to be set to public or unlisted to be downloaded."
          "\nInput the URL of the playlist or single to download:")
    usrInput = input("\nURL: ").strip()
    
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


def audioOrVideo(): #Function for specifying audio or video download
    print("\nWhich do you want to download:"
          "\n1) Audio (mp3)"
          "\n2) Video (mp4)"
          "\n3) Advanced (Custom Format)")
    
    if (temp:=input("Input: ")) == "1": #If audio
        return "bestaudio[ext=mp3]/best" #Return parameters for audio - mp3 and best quality
    elif temp == "2": #If video
        return "bestvideo[ext=mp4]+bestaudio[ext=mp4]/best" #Return parameters for video - mp4 and best quality
    elif temp == "3": #If custom format
        return customFormat() #Return custom format
    else:
        print("Invalid Input")
        audioOrVideo()
    
        
def customFormat(): #Function for setting custom format
    print("\nDo you want to download"
          "\n1) Audio"
          "\n2) Video")
    
    #Player picks audio or video
    if (usrInput:=input("Input: ").strip()) == "1": #If audio
        while True: 
            audioFormats = ["mp3", "m4a", "mp4", "wav", "aac", "flac", "ogg", "opus", "vorbis", "wma", "alac", "webm", "mkv", "mka"] #List of supported audio formats
            print("\nWhich format do you want to download:" 
                "\nSupported Formats are: ", audioFormats)
            
            temp=input("Input: ").strip() #Player picks format
            if temp in audioFormats: #If format is supported
                fileFormat = f"ext={temp}" #Set format
                break
            else:
                print("Invalid Input")
            
        custQuality = customQuality(usrInput) #Return custom quality
        return f"{custQuality}audio[{fileFormat}]/best" #Return custom quality and format parameter
    
    if usrInput == "2": #If video
        while True: 
            videoFormats = ["mp4", "flv", "ogg", "webm", "mkv", "avi", "mov"] #List of supported video formats
            print("\nWhich format do you want to download:"
                  "\nSupported Formats are: ", videoFormats)
            
            temp=input("Input: ").strip() #Player picks format
            if temp in videoFormats: #If format is supported
                fileFormat = f"ext={temp}" #Set format
                break
            else:
                print("Invalid Input")
        
        custQuality, custResolution = customQuality(usrInput) #Return custom quality
        return f"{custQuality}video{custResolution}[{fileFormat}]+bestaudio[ext=m4a]/best" #Return custom quality and format parameter


def customQuality(type): #Function for setting custom quality - Passed type of download (audio or video)
    while True: 
            print("\nWhich quality do you want to download:"
                "\n1) Best"
                "\n2) Worst")
            if (temp:=input("Input: ")) == "1": #If best quality
                quality = "best" #Set quality
                break
            elif temp == "2": #If worst quality
                quality = "worst" #Set quality
                break
            else:
                print("Invalid Input")
                
    if type == "1": #If audio
        return quality #Return quality (resolution isnt needed for audio)
                    
    
    validResolutions = ["144", "240", "360", "480", "720", "1080", "1440", "2160", "4320"] #List of valid resolutions
    while True:
        temp = input("\nInput Resolution (e.g. 720, 1080)"
                     "\nInput Blank for Best: ")
        
        if temp in validResolutions: #If resolution is valid
            resolution = f"[height<={temp}]" #Set resolution
            break
        elif temp == "": #If blank
            resolution = "" #Set resolution to blank (defualt - best)
            break
        else:
            print("Invalid Input")
                
    return quality, resolution #Return quality and resolution

    
def my_hook(d):
    if d['status'] == 'finished':
        print("\nFinished downloading: ", d['filename'])

Download()